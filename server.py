import sys
import asyncio
import socketio
from aiohttp import web
import json
import signal
import sys
import os
import os.path
import hashlib
import markdown2
import bs4
import base64
import re

# sio = socketio.AsyncServer(logger=True, async_mode='aiohttp', cors_allowed_origins='*')

# @sio.event
# async def connect(sid, environ):
#     print('connect', sid)

# container keeps a container running (with --restart=always)
# container keeps service commands running (when they terminate, restart them)
# container wrapper process? with fixed file descriptors for the commands
# monitor docker events

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

# async def get_docker_events(queue: asyncio.Queue) -> None:
#     async def read_stdout(stdout: asyncio.StreamReader, queue: asyncio.Queue) -> None:
#         while True:
#             buffer = await stdout.readline()
#             if not buffer:
#                 break
#             await queue.put(json.loads(buffer))

#     async def read_stderr(stderr: asyncio.StreamReader) -> None:
#         while True:
#             buffer = await stderr.readline()
#             if not buffer:
#                 break
#             sys.stderr.write(buffer)

#     process = await asyncio.create_subprocess_exec('docker', 'events', '--format={{json .}}', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
#     print(process)

#     read_stdout_task = asyncio.create_task(read_stdout(process.stdout, queue))
#     read_stderr_task = asyncio.create_task(read_stderr(process.stderr))
#     process_task = asyncio.create_task(process.wait())

#     # this will return when e.g. the docker process dies
#     # therefore skipping error handling here and let exceptions bring the parent process down
#     await asyncio.gather(read_stdout_task, read_stderr_task, process_task)


# async def print_events(queue: asyncio.Queue) -> None:
#     while True:
#         event = await queue.get()
#         if event is None:
#             break
#         print(event)
#         # skipping queue.task_done() because this queue has infinite life-time


# async def main():
#     def terminate():
#         print('Terminating ...')
#         for task in asyncio.all_tasks():
#             task.cancel()

#     asyncio.get_running_loop().add_signal_handler(signal.SIGINT, terminate)
#     asyncio.get_running_loop().add_signal_handler(signal.SIGTERM, terminate)

#     try:
#         queue = asyncio.Queue()

#         producer = asyncio.create_task(get_docker_events(queue))
#         consumer = asyncio.create_task(print_events(queue))

#         await asyncio.gather(producer, consumer)
#     except asyncio.CancelledError:
#         pass


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

# TODO: channel class with zero size queue

def get_pages(pages_path):
    pages_path = os.path.abspath(pages_path)
    pages = []
    for root_path, _, filenames in os.walk(pages_path):
        for file in [file for file in filenames if os.path.splitext(file)[1] == '.md']:
            markdown_path = os.path.join(root_path, file)
            # generate base URL: 1. dirname of markdown_path, 2. remove pages directory prefix, 3. make the path absolute to root it in webroot, 4. normalize path (remove '.' and '..')
            base_url = os.path.normpath(os.path.join(os.path.abspath(
                os.sep), os.path.relpath(root_path, start=pages_path)))
            page = {
                'base_url': base_url,
                'url': os.path.join(base_url, f'{os.path.splitext(file)[0]}.html'),
            }
            page['hash'] = hashlib.sha256(page['url'].encode('utf-8')).hexdigest()
            with open(markdown_path) as f:
                markdown = f.read()
                raw_html = markdown2.markdown(markdown)
                soup = bs4.BeautifulSoup(raw_html, 'html.parser')

                # build array of found static files (any other file requests will yield an error)
                static_files = []
                for img in soup.find_all('img'):
                    if not os.path.realpath(os.path.join(pages_path, os.path.relpath(base_url, start=os.path.abspath(os.path.sep)), img['src'])).startswith(pages_path):
                        raise ValueError(
                            f'{img} escapes path {pages_path} (from {markdown_path})')
                    static_files.append(os.path.join(base_url, img['src']))

                # replace custom tags with boilerplate code
                widgets = []
                widget_counter = 0
                for button in soup.find_all('x-button'):
                    widget = {
                        'hash': hashlib.sha256(f'{widget_counter}-{button.string}-{button["command"]}'.encode('utf-8')).hexdigest(),
                        'type': 'button',
                        'command': button['command'],
                        'title': button.string,
                        'is_long_running': False,
                        'count': widget_counter,
                    }
                    widget_counter += 1

                    paragraph = soup.new_tag('p')
                    b = soup.new_tag('b')
                    b.string = 'Button'
                    paragraph.append(b)
                    paragraph.append(' with text ')
                    b = soup.new_tag('b')
                    b.string = button.string
                    paragraph.append(b)
                    paragraph.append(' for ')
                    code = soup.new_tag('code')
                    code.string = button['command']
                    paragraph.append(code)
                    paragraph.append(' with ID ')
                    code = soup.new_tag('code')
                    code.string = widget['hash']
                    paragraph.append(code)
                    button.replace_with(paragraph)

                    widgets.append(widget)
                # for editor in soup.find_all('x-editor'):
                #     editor.replace_with(generate_editor(soup, editor))
                # for terminal in soup.find_all('x-terminal'):
                #     terminal.replace_with(generate_terminal(soup, terminal))

                html = soup.encode(formatter='html5').decode('utf-8')

                page.update({
                    'markdown': markdown,
                    'static_files': static_files,
                    'widgets': widgets,
                    'html': html,
                })

            dockerfile_path = os.path.join(root_path, 'Dockerfile')
            image_name_suffix = re.sub(r'[^a-z0-9]', '-', base_url.lower())
            try:
                open(dockerfile_path)
                page.update({
                    'dockerfile': dockerfile_path,
                    'image_name': f'recruiting-website-{image_name_suffix}',
                })
            except OSError as e:
                # TODO: if e.errno == 2: pass
                print(f'Skipping to build a docker image: {str(e)}')

            pages.append(page)

    return pages


class WorkerController:
    """tries to run all required containers and receives data from proxy"""

    def __init__(self, pages):
        self.pages = pages
        self.event = asyncio.Event()
        self.running_workers = {}
        self.requested_workers = {}
        pass

    async def build_images(self):
        for page in self.pages:
            try:
                print(f'Building {page["dockerfile"]} ...')

                process = await asyncio.create_subprocess_exec('docker', 'build', '--pull', '--tag', page['image_name'], os.path.dirname(page['dockerfile']))

                await process.wait()

                if process.returncode != 0:
                    raise RuntimeError('Failed to build docker image')
            except KeyError:
                pass

    async def run(self):
        asyncio.create_task(self.read_docker_events())
        # init: collect running containers
        # diff the requested againts running workers
        while True:
            await self.event.wait()
            self.event.clear()
            await self.update_running_docker_containers()
            to_create, to_remove = self.diff_workers()
            for worker in to_create:
                await self.start_worker(worker)
            for worker in to_remove:
                await self.stop_worker(worker)
        # apply changes: start, stop containers and processes
        # also: forward IO
        pass

    async def stdout_of(self, *args):
        process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE)
        print(*args, process)

        stdout, _ = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f'Failed to run command: {" ".join(args)}')

        return stdout

    async def update_running_docker_containers(self):
        container_ids = await self.stdout_of('docker', 'container', 'ls', '--all', '--format={{json .ID}}')

        if len(container_ids) == 0:
            self.running_workers = []
            return

        container_ids = [json.loads(container_id)
                         for container_id in container_ids.splitlines()]
        container_metadata = json.loads(await self.stdout_of('docker', 'inspect', *container_ids))

        running_workers = {}
        for metadata in container_metadata:
            name = re.match(
                r'/recruiting-website-([A-Za-z0-9-]+)', metadata['Name'])
            if name is not None and metadata['State']['Running'] and not metadata['State']['Paused']:
                running_workers[name.group(1)] = {
                    'id': metadata['Id'],
                }
        self.running_workers = running_workers

    async def start_worker(self, worker_uuid):
        pass

    async def stop_worker(self, worker_uuid):
        pass

    def diff_workers(self):
        return \
            set(self.requested_workers.keys()) - set(self.running_workers.keys()), \
            set(self.running_workers.keys()) - set(self.requested_workers.keys())

    async def read_docker_events(self):
        async def read_stdout(self, stdout: asyncio.StreamReader):
            while True:
                buffer = await stdout.readline()
                if not buffer:
                    break
                # currently ignore the buffer (use the buffer in the future to update the running containers)
                self.event.set()

        process = await asyncio.create_subprocess_exec('docker', 'events', '--format={{json .}}', stdout=asyncio.subprocess.PIPE)
        print(process)

        read_stdout_task = asyncio.create_task(
            read_stdout(self, process.stdout))
        process_task = asyncio.create_task(process.wait())

        # this will return when e.g. the docker process dies
        # therefore skipping error handling here and let exceptions bring the parent process down
        # await asyncio.gather(read_stdout_task, read_stderr_task, process_task)

    def create_worker(self, worker_uuid, page_hash, channels):
        # mutate requested workers
        self.requested_workers[worker_uuid] = {
            'page_hash': page_hash,
            'commands': [],  # TODO: get commands
            'channels': channels,
        }
        pass

    def remove_worker(self, worker_uuid):
        # mutate requested workers
        del self.requested_workers[worker_uuid]
        pass


class ClientConnector:
    """coordinates IO between clients and workers"""

    def __init__(self, worker_controller: WorkerController, generated_data, commands):
        # stored clients, reference counting for workers
        self.worker_controller = worker_controller
        self.clients = {}
        self.workers = {}
        pass

    async def run(self):
        # TODO: forward IO, needed, because tasks are forwarding IO
        pass

    def create_client(self, client_uuid, worker_uuid, page_hash, channels):
        self.clients[client_uuid] = {
            'worker': worker_uuid,
            'channels': channels,
        }
        try:
            self.workers[worker_uuid]['reference_count'] += 1
        except KeyError:
            # TODO: generate new channels for worker (each command 3 channels: stdin, stdout, stderr)
            # TODO: read from generated commands
            # TODO: create tasks for each channel (maybe only create stdin task here, stdout/stderr will be started at the client channels)
            # TODO: store tasks in the dicts
            self.workers[worker_uuid] = {
                'reference_count': 1,
                'channels': channels,
            }
            self.worker_controller.create_worker(worker_uuid, page_hash)

    def remove_client(self, client_uuid):
        worker_uuid = self.clients[client_uuid]['worker']
        self.workers[worker_uuid]['reference_count'] -= 1
        if self.workers[worker_uuid]['reference_count'] == 0:
            # TODO: cancel channel tasks
            del self.workers[worker_uuid]
            self.worker_controller.remove_worker(worker_uuid)


class Proxy:
    """serves static files and connects clients"""

    def __init__(self, client_connector, generated_data, commands):
        pass

    async def run(self):
        pass


async def main():
    pages = get_pages('pages')
    worker_controller = WorkerController(pages)
    # await worker_controller.build_images()
    await worker_controller.update_running_docker_containers()
    print(worker_controller.running_workers)


if __name__ == '__main__':
    # web.run_app(app)
    # asyncio.run(run('docker ps --all'))
    # asyncio.run(start('12356787654323456754323456'))
    # asyncio.run(run('docker ps --all'))
    # import pprint
    # pprint.pprint(pages)
    asyncio.run(main())
