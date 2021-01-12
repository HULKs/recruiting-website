import os
import os.path
import sys
import hashlib
import markdown2
import bs4
import re
from aiohttp import web
import asyncio
import socketio


class StaticPage:
    def __init__(self, pages_path: str, url: str, page_path: str):
        self.pages_path = pages_path
        self.url = url
        self.page_path = page_path
        self.markdown_path = os.path.join(page_path, 'page.md')
        with open(self.markdown_path) as f:
            self.markdown = f.read()
        self.html = markdown2.markdown(self.markdown)
        self.routes = [
            web.get(self.url, self.serve_index),
            web.get('/favicon.ico', self.serve_file),
        ]

        soup = bs4.BeautifulSoup(self.html, 'html.parser')
        for img in soup.find_all('img'):
            # TODO: check if static files escape pages directory
            self.routes.append(web.get(os.path.realpath(
                os.path.join(url, img['src'])), self.serve_file))
        html = soup.new_tag('html')
        head = soup.new_tag('head')
        html.append(head)
        title = soup.new_tag('title')
        title.string = 'HULKs Recruiting Website'
        head.append(title)
        body = soup.new_tag('body')
        for child in soup.contents:
            body.append(child.extract())
        html.append(body)
        soup.append(bs4.Doctype('html'))
        soup.append(html)
        self.html = soup.encode(formatter='html5').decode('utf-8')

    def __repr__(self):
        return f'<StaticPage url=\'{self.url}\'>'

    async def serve_index(self, request: web.Request):
        return web.Response(text=self.html, content_type='text/html')

    async def serve_file(self, request: web.Request):
        path = os.path.realpath(os.path.join(self.pages_path, os.path.relpath(
            request.path, start=os.path.abspath(os.path.sep))))
        return web.FileResponse(path=path)


class InteractivePage(StaticPage, socketio.AsyncNamespace):
    def __init__(self, pages_path: str, url: str, page_path: str):
        StaticPage.__init__(self, pages_path, url, page_path)
        socketio.AsyncNamespace.__init__(self, namespace=url)
        self.hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        self.image_name = f'recruiting-website-{self.hash}'
        self.clients = {}
        self.containers = {}
        self.volumes = []
        self.widgets = {}

        soup = bs4.BeautifulSoup(self.html, 'html.parser')
        for i, element in enumerate(soup.find_all('x-button')):
            widget = ButtonWidget(self, i, element)
            element.replace_with(widget.get_replacement(soup))
            self.widgets[widget.hash] = widget
        if len(self.widgets) > 0:
            self.routes.append(web.get('/socket.io.js', self.serve_file))
            soup.head.append(soup.new_tag('script', src='/socket.io.js'))
            connect_script = soup.new_tag('script')
            connect_script.string = f'''
                const uuidv4 = () => {{
                    // https://gist.github.com/outbreak/316637cde245160c2579898b21837c1c
                    const getRandomSymbol = (symbol) => {{
                        var array;
                        if (symbol === 'y') {{
                            array = ['8', '9', 'a', 'b'];
                            return array[Math.floor(Math.random() * array.length)];
                        }}
                        array = new Uint8Array(1);
                        window.crypto.getRandomValues(array);
                        return (array[0] % 16).toString(16);
                    }}
                    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, getRandomSymbol);
                }}
                // https://gist.github.com/johnelliott/cf77003f72f889abbc3f32785fa3df8d
                if (!location.hash.match(new RegExp(/^#[0-9A-F]{{8}}-[0-9A-F]{{4}}-4[0-9A-F]{{3}}-[89AB][0-9A-F]{{3}}-[0-9A-F]{{12}}$/i))) {{
                    location.hash = `#${{uuidv4()}}`;
                }}
                const uuid = location.hash.substr(1);
                const socket = io('{self.url}');
                socket.on('connect', () => {{
                    console.log('connect');
                    socket.emit('set_uuid', uuid);
                }});
                let buttonCallbacks = {{}};
                socket.on('button_response', data => {{
                    console.log(data);
                    if (data.hash && buttonCallbacks[data.hash]) {{
                        buttonCallbacks[data.hash](data);
                    }} else {{
                        console.error('Failed to send to widget', data);
                    }}
                }});
                socket.on('disconnect', () => {{
                    console.log('disconnect');
                }});
            '''
            soup.head.append(connect_script)
        self.html = soup.encode(formatter='html5').decode('utf-8')

    def __repr__(self):
        return f'<InteractivePage url=\'{self.url}\'>'

    def on_connect(self, sid: str, environment):
        print(f'{sid} connected')

    async def on_set_uuid(self, sid: str, uuid):
        print(f'{sid} set uuid {uuid}')
        if re.match(r'[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}', uuid, flags=re.IGNORECASE) is None:
            raise RuntimeError(f'Invalid UUID from {sid}: {uuid}')
        self.enter_room(sid, uuid)
        self.clients[sid] = uuid
        # TODO: race condition possible
        if uuid not in self.volumes:
            self.volumes.append(uuid)
            await self.create_volume(uuid)
        # if uuid not in self.containers:
        #     self.containers[uuid] = Container(self, uuid)

    async def on_disconnect(self, sid: str):
        print(f'{sid} disconnected')
        uuid = self.clients[sid]
        del self.clients[sid]
        remaining_clients = sum(
            [1 for client_uuid in self.clients.values() if client_uuid == uuid])
        if remaining_clients == 0:
            # TODO: race condition possible
            self.volumes.remove(uuid)
            await self.remove_volume(uuid)

    async def on_button_click(self, sid: str, data):
        print(f'Button click of {sid}:', data)
        uuid = self.clients[sid]
        try:
            widget_hash = data['hash']
            # try:
            response = await self.widgets[widget_hash].on_click(uuid)
            response['hash'] = widget_hash
            print('response:', response)
            await self.emit('button_response', response)
            # except (KeyError, AttributeError):
            #     print(
            #         f'Failed to send click to {widget_hash} (no widget or wrong type)', data, file=sys.stderr)
        except KeyError:
            print(f'Failed to extract hash of widget', data, file=sys.stderr)

    async def build_image(self):
        print(f'Building container image for {self.page_path} ...')
        process = await asyncio.create_subprocess_exec('docker', 'build', '--pull', '--tag', self.image_name, self.page_path)
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError('Failed to build docker image')

    def runtime_hash(self, uuid: str):
        return hashlib.sha256(f'{self.hash}-{uuid}'.encode('utf-8')).hexdigest()

    def get_volume_name_by_uuid(self, uuid: str):
        return f'recruiting-website-{self.runtime_hash(uuid)}'

    async def create_volume(self, uuid: str):
        print(f'Creating volume for {uuid} ...')
        process = await asyncio.create_subprocess_exec('docker', 'volume', 'create', self.get_volume_name_by_uuid(uuid))
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError('Failed to create docker volume')

    async def remove_volume(self, uuid: str):
        print(f'Removing volume for {uuid} ...')
        process = await asyncio.create_subprocess_exec('docker', 'volume', 'rm', self.get_volume_name_by_uuid(uuid))
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError('Failed to remove docker volume')


class Container:
    def __init__(self, page: InteractivePage, uuid: str):
        self.page = page
        self.uuid = uuid
        self.container_name = f'recruiting-website-{self.page.hash}-{self.uuid}'
        self.stop_event = asyncio.Event()
        print(uuid, 'starting container ...')
        self.task = asyncio.create_task(self.container())

    async def container(self):
        print(self.uuid, 'entering container loop')

        while True:
            # https://stackoverflow.com/a/35770783
            process = await asyncio.create_subprocess_exec(
                'docker',
                'run',
                '--rm',
                '--name', self.container_name,
                '--network=none', self.page.image_name,
                'sh',
                '-c',
                'trap : TERM INT; (while true; do sleep 86400; done) & wait'
            )

            process_task = asyncio.create_task(process.wait())
            stop_task = asyncio.create_task(self.stop_event.wait())

            print(self.uuid, process, 'listening for state changes ...')
            done, _ = await asyncio.wait([process_task, stop_task], return_when=asyncio.FIRST_COMPLETED)

            if stop_task in done:
                process.terminate()
                print(self.uuid, process,
                      'waiting to terminate (timeout: 5s) ...')
                await asyncio.wait_for(process_task, timeout=5.0)
                print(self.uuid, process, 'testing if terminated ...')
                if process.returncode is None:
                    print(self.uuid, process,
                          'kill because not terminated yet ...')
                    process.kill()
                break

            print(self.uuid, process, 'terminated, restarting ...')
            stop_task.cancel()

        print(self.uuid, 'exiting container loop')

    async def stop(self):
        print(self.uuid, 'stopping container ...')
        self.stop_event.set()
        await self.task


class ButtonWidget:
    def __init__(self, page: InteractivePage, i: int, element):
        self.page = page
        self.title = element.string
        self.command = element['command']
        self.hash = hashlib.sha256(f'{self.page.hash}-{self.title}-{self.command}-{i}'.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'<ButtonWidget title=\'{self.title}\', command=\'{self.command}\'>'

    def get_replacement(self, soup):
        replacement = soup.new_tag('div')
        h1 = soup.new_tag('h1')
        h1.string = 'Button'
        replacement.append(h1)
        button = soup.new_tag('button', onClick=f'buttonClick_{self.hash}()')
        button.string = self.title
        replacement.append(button)
        output = soup.new_tag('div', id=f'button-output-{self.hash}')
        replacement.append(output)
        script = soup.new_tag('script')
        script.string = f'''
            const buttonClick_{self.hash} = () => {{
                console.log('Click of {self.hash}');
                socket.emit('button_click', {{ 'hash': '{self.hash}' }});
            }};
            buttonCallbacks['{self.hash}'] = data => {{
                console.log('Got response:', data);
                if (data.stdout) {{
                    document.getElementById('button-output-{self.hash}').innerText = data.stdout;
                }}
            }};
        '''
        replacement.append(script)
        return replacement

    def runtime_hash(self, uuid: str):
        return hashlib.sha256(f'{self.hash}-{uuid}'.encode('utf-8')).hexdigest()

    def get_container_name_by_uuid(self, uuid: str):
        return f'recruiting-website-{self.runtime_hash(uuid)}'

    async def on_click(self, uuid: str):
        print(f'got click, waiting 1s ...')
        process = await asyncio.create_subprocess_exec(
            'docker',
            'run',
            '--rm',
            '--name', self.get_container_name_by_uuid(uuid),
            '--network=none',
            '--mount', f'src={self.page.get_volume_name_by_uuid(uuid)},dst=/data',
            self.page.image_name,
            'sh',
            '-c',
            self.command,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        print(self.command, process)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f'Failed to run command: {self.command}')
        print(f'sending response ...')
        return {
            'stdout': stdout.decode('utf-8'), 
            'stderr': stderr.decode('utf-8'),
        }


def get_pages(sio, pages_path):
    pages_path = os.path.abspath(pages_path)
    pages = []
    for page_path, _, filenames in os.walk(pages_path):
        if 'page.md' in filenames:
            # generate URL '/some/page' from absolute page path '/.../pages/some/page':
            # 1. remove pages directory prefix
            # 2. make the path absolute to root it in webroot
            # 3. normalize path (remove '.' and '..')
            url = os.path.normpath(os.path.join(os.path.abspath(
                os.sep), os.path.relpath(page_path, start=pages_path)))
            dockerfile_path = os.path.join(page_path, 'Dockerfile')
            try:
                # test to open Dockerfile
                open(dockerfile_path)
                page = InteractivePage(pages_path, url, page_path)
                pages.append(page)
            except OSError as e:
                # errno 2: No such file or directory
                if e.errno != 2:
                    raise
                page = StaticPage(pages_path, url, page_path)
                pages.append(page)
    return pages


async def app_factory():
    sio = socketio.AsyncServer(
        logger=True, async_mode='aiohttp', cors_allowed_origins='*')
    app = web.Application()
    sio.attach(app)
    pages = get_pages(sio, 'pages')
    print('pages:')
    for page in pages:
        print(' ', page)
        print('    routes:', page.routes)
        app.add_routes(page.routes)
        if isinstance(page, InteractivePage):
            sio.register_namespace(page)
            print('    widgets:', page.widgets)
            await page.build_image()
    return app


if __name__ == '__main__':
    web.run_app(app_factory())
