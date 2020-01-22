import sys
import asyncio
import socketio
from aiohttp import web
import json
import signal

# sio = socketio.AsyncServer(logger=True, async_mode='aiohttp', cors_allowed_origins='*')

# @sio.event
# async def connect(sid, environ):
#     print('connect', sid)

# container keeps a container running (with --restart=always)
# container keeps service commands running (when they terminate, restart them)
# container wrapper process? with fixed file descriptors for the commands
# monitor docker events


# initial state:
# - no containers running
# - directory structure with Markdown and Dockerfiles
# startup:
# - start proxy container (with docker UNIX socket mounted)
# - proxy generates HTML from Markdown
#   - possibly with https://github.com/trentm/python-markdown2 and BeautifulSoup4
#   - store metadata informations for later (which commands, generate UUIDs for them)
# - proxy generates HTML server routes for directory structure
# - proxy generates Socket.IO event handlers for all different types of widgets
# initial state:
# - proxy listens for HTTP+Socket.IO
# - no workers running
# user requests a page in the directory structure:
# - user GET /path/in/directory/structure
# - proxy serves generated HTML and static files
# - user executes JavaScript
#   - if has no UUID, generates a new random UUIDv4
#   - connects via Socket.IO
#   - announces chosen UUID to proxy
# - proxy puts user into a room with the UUID
# - proxy starts a worker container
#   - starts an idle container
#   - executes all long running commands
# - proxy sets up IO piping
# user requests a static page (e.g. index):
# - user GET /path/to/index
# - proxy serves generated HTML and/or static files


# class Container:
#     """Container represents a docker container. It has the following states: SCHEDULED, STARTED, COMMANDS_RUNNING, STOPPED"""
#     def __init__(self, image_name, commands):
#         self.state = 'SCHEDULED'
#         self.image_name = image_name
#         self.commands = commands

# class ContainerClaim:
#     """ContainerClaim represents a claim on a container. The class' task is to ensure a running container."""
#     def __init__(self, uuid,):
#         pass

# class Store:
#     """Store stores clients and containers."""
#     def __init__(self):
#         self.clients = {}
#         self.containers = set()

#     def client_upsert(self, client, uuid):
#         self.clients[client] = uuid
#         self.update_claims()

#     def client_delete(self, client):
#         del self.clients[client]
#         self.update_claims()

#     def update_claims(self):
#         requested = set(self.clients.values())
#         to_create = requested - self.containers
#         to_remove = self.containers - requested


# clients = {}

# @sio.event
# async def disconnect(sid):
#     print('disconnect', sid)
#     del clients[sid]

# @sio.event
# async def set_uuid(sid, uuid):
#     print('set_uuid', sid, uuid)
#     sio.enter_room(sid, uuid)
#     clients[sid] = uuid


# app = web.Application()
# sio.attach(app)

# app.router.add_static('/', 'static')

# containers = []


# async def start(uuid):
#     process = await asyncio.create_subprocess_exec(
#         'docker',
#         'run',
#         '--name', f'recruiting-website-worker-{uuid}',
#         '--detach',
#         '--network=none',
#         'ubuntu:18.04',
#         '/bin/sleep',
#         '60',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     stdout, stderr = await process.communicate()

#     print(f'command exited with {process.returncode}')
#     print(stdout, stderr)

#     if process.returncode == 0 and len(stdout) > 0 and len(stderr) == 0:
#         sys.stdout.write(stdout)
#         return stdout.decode('utf-8')
#     else:
#         sys.stderr.write(stderr)


# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)

#     stdout, stderr = await proc.communicate()

#     print(f'[{cmd!r} exited with {proc.returncode}]')
#     if stdout:
#         print(f'[stdout]\n{stdout.decode()}')
#     if stderr:
#         print(f'[stderr]\n{stderr.decode()}')

async def get_docker_events(queue: asyncio.Queue) -> None:
    async def read_stdout(stdout: asyncio.StreamReader, queue: asyncio.Queue) -> None:
        while True:
            buffer = await stdout.readline()
            if not buffer:
                break
            await queue.put(json.loads(buffer))

    async def read_stderr(stderr: asyncio.StreamReader) -> None:
        while True:
            buffer = await stderr.readline()
            if not buffer:
                break
            sys.stderr.write(buffer)

    process = await asyncio.create_subprocess_exec('docker', 'events', '--format={{json .}}', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    print(process)

    read_stdout_task = asyncio.create_task(read_stdout(process.stdout, queue))
    read_stderr_task = asyncio.create_task(read_stderr(process.stderr))
    process_task = asyncio.create_task(process.wait())

    # this will return when e.g. the docker process dies
    # therefore skipping error handling here and let exceptions bring the parent process down
    await asyncio.gather(read_stdout_task, read_stderr_task, process_task)


async def print_events(queue: asyncio.Queue) -> None:
    while True:
        event = await queue.get()
        if event is None:
            break
        print(event)
        # skipping queue.task_done() because this queue has infinite life-time


async def main():
    def terminate():
        print('Terminating ...')
        for task in asyncio.all_tasks():
            task.cancel()

    asyncio.get_running_loop().add_signal_handler(signal.SIGINT, terminate)
    asyncio.get_running_loop().add_signal_handler(signal.SIGTERM, terminate)

    try:
        queue = asyncio.Queue()

        producer = asyncio.create_task(get_docker_events(queue))
        consumer = asyncio.create_task(print_events(queue))

        await asyncio.gather(producer, consumer)
    except asyncio.CancelledError:
        pass


if __name__ == '__main__':
    # web.run_app(app)
    # asyncio.run(run('docker ps --all'))
    # asyncio.run(start('12356787654323456754323456'))
    # asyncio.run(run('docker ps --all'))
    asyncio.run(main())
