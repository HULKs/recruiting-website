import mkdocs
import os
import pathlib


log = mkdocs.plugins.log.getChild('recruiting-website-navigation')


class Plugin(mkdocs.plugins.BasePlugin):

    def on_nav(self, nav: mkdocs.structure.nav.Navigation, config: mkdocs.config.base.Config, files: mkdocs.structure.files.Files) -> mkdocs.structure.nav.Navigation:
        return files

    def on_page_context(self, context: dict, page: mkdocs.structure.pages.Page, config: mkdocs.config.base.Config, nav: mkdocs.structure.files.Files) -> dict:
        files = {
            pathlib.PurePosixPath('/') / file.url: file
            for file in nav if file.is_documentation_page()
        }
        page_url = pathlib.PurePosixPath('/') / page.url
        parents = [
            {
                'url': os.path.relpath(parent_url, page_url),
                'title': files[parent_url].page.title,
            }
            for parent_url in sorted(page_url.parents, key=lambda parent_url: len(str(parent_url)))
        ]
        children = [
            {
                'url': os.path.relpath(file_url, page_url),
                'title': file.page.title,
            }
            for file_url, file in sorted(files.items(), key=lambda item: len(str(item[0])))
            if file_url.parent != file_url and file_url.parent == page_url
        ]
        return {
            **context,
            **{
                'parents': parents,
                'children': children,
            },
        }
