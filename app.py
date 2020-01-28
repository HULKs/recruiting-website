import os
import os.path
import hashlib
import markdown2
import bs4
import re
from aiohttp import web
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
        self.connected_clients = 0
        self.widgets = {}
        
        soup = bs4.BeautifulSoup(self.html, 'html.parser')
        for i, element in enumerate(soup.find_all('x-button')):
            widget = ButtonWidget(self, i, element)
            element.replace_with(widget.get_replacement(soup))
            self.widgets[widget.hash] = widget
        if len(self.widgets) > 0:
            self.routes.append(web.get('/socket.io.js', self.serve_file))
            soup.head.append(soup.new_tag('script', src='/socket.io.js'))
        self.html = soup.encode(formatter='html5').decode('utf-8')

    def __repr__(self):
        return f'<InteractivePage url=\'{self.url}\'>'

    def on_set_uuid(self, sid: str, uuid):
        print(f'{sid} set uuid {uuid}')
        self.enter_room(sid, uuid)
        self.connected_clients += 1
        if self.connected_clients > 1:
            print(f'attach {sid} to worker {uuid}')
        else:
            print(f'start worker {uuid} for {sid}')

    def on_disconnect(self, sid: str):
        print(f'{sid} disconnected')
        self.connected_clients -= 1
        if self.connected_clients > 0:
            print(f'detach {sid} from worker')
        else:
            print(f'stop worker from {sid}')


class ButtonWidget:
    def __init__(self, page: InteractivePage, i: int, element):
        self.page = page
        self.title = element.string
        self.command = element['command']
        self.hash = hashlib.sha256(
            f'{self.page.hash}-{self.title}-{self.command}-{i}'.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'<ButtonWidget title=\'{self.title}\', command=\'{self.command}\'>'

    def get_replacement(self, soup):
        replacement = soup.new_tag('div')
        h1 = soup.new_tag('h1')
        h1.string = 'Button'
        replacement.append(h1)
        button = soup.new_tag('button')
        button.string = self.title
        replacement.append(button)
        script = soup.new_tag('script')
        script.string = '''
            console.log("Hello World from Python!");
            console.log("Another line!");
        '''
        replacement.append(script)
        return replacement


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


if __name__ == '__main__':
    sio = socketio.AsyncServer(
        logger=True, async_mode='aiohttp', cors_allowed_origins='*')
    app = web.Application()
    sio.attach(app)
    pages = get_pages(sio, 'pages')
    print('pages:')
    for page in pages:
        print(' ',page)
        if isinstance(page, InteractivePage):
            sio.register_namespace(page)
            print('    widgets:', page.widgets)
        print('    routes:', page.routes)
        app.add_routes(page.routes)
    web.run_app(app)
