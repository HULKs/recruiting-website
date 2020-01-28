import os
import os.path
import hashlib
import markdown2
import bs4
import re
from aiohttp import web
import socketio

class StaticPage:
    def __init__(self, url: str, page_path: str):
        self.url = url
        self.routes = [
            web.get(self.url, self.serve_index),
        ]
        self.page_path = page_path
        self.markdown_path = os.path.join(page_path, 'page.md')
        with open(self.markdown_path) as f:
            self.markdown = f.read()
        self.html = markdown2.markdown(self.markdown)
        # TODO: check static files
        # soup = bs4.BeautifulSoup(self.html, 'html.parser')
        # self.static_files = []
        # for img in soup.find_all('img'):
        #     self.static_files.append(os.path.realpath(os.path.join(url, img['src'])))
    
    async def serve_index(self, request):
        return web.Response(text=self.html, content_type='text/html')

class InteractivePage(StaticPage, socketio.AsyncNamespace):
    def __init__(self, url: str, page_path: str):
        StaticPage.__init__(self, url, page_path)
        socketio.AsyncNamespace.__init__(self, namespace=url)
        self.connected_clients = 0
        self.widgets = {}
        # soup = bs4.BeautifulSoup(self.html, 'html.parser')
    
    def on_set_uuid(self, sid, uuid):
        print(f'{sid} set uuid {uuid}')
        self.enter_room(sid, uuid)
        self.connected_clients += 1
        if self.connected_clients > 1:
            print(f'attach {sid} to worker {uuid}')
        else:
            print(f'start worker {uuid} for {sid}')
    
    def on_disconnect(self, sid):
        print(f'{sid} disconnected')
        self.connected_clients -= 1
        if self.connected_clients > 0:
            print(f'detach {sid} from worker')
        else:
            print(f'stop worker from {sid}')

# class ButtonWidget:
    

def get_pages(sio, pages_path):
    pages_path = os.path.abspath(pages_path)
    pages = []
    for page_path, _, filenames in os.walk(pages_path):
        if 'page.md' in filenames:
            # generate URL '/some/page' from absolute page path '/.../pages/some/page':
            # 1. remove pages directory prefix
            # 2. make the path absolute to root it in webroot
            # 3. normalize path (remove '.' and '..')
            url = os.path.normpath(os.path.join(os.path.abspath(os.sep), os.path.relpath(page_path, start=pages_path)))
            dockerfile_path = os.path.join(page_path, 'Dockerfile')
            try:
                # test to open Dockerfile
                open(dockerfile_path)
                page = InteractivePage(url, page_path)
                pages.append(page)
            except OSError as e:
                if e.errno != 2:
                    raise
                page = StaticPage(url, page_path)
                pages.append(page)
    return pages

if __name__ == '__main__':
    sio = socketio.AsyncServer(logger=True, async_mode='aiohttp', cors_allowed_origins='*')
    app = web.Application()
    sio.attach(app)
    pages = get_pages(sio, 'pages')
    print('pages:')
    for page in pages:
        print(' ', page.url, page)
        if isinstance(page, InteractivePage):
            sio.register_namespace(page)
        print('    routes:', page.routes)
        app.add_routes(page.routes)
    web.run_app(app)
