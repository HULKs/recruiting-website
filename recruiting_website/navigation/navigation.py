import mkdocs

print(mkdocs.__dict__)



log = mkdocs.plugins.log.getChild('recruiting-website')


class Plugin(mkdocs.plugins.BasePlugin):

    def on_nav(self, nav: mkdocs.structure.nav.Navigation, config: mkdocs.config.base.Config, files: mkdocs.structure.files.Files) -> mkdocs.structure.nav.Navigation:
        for item in nav.items:
            log.info(item)
        for page in nav.pages:
            log.info(page)
        log.info('Files')
        for file in files:
            if file.is_documentation_page():
                log.info(f'Documentation Page: {file.src_path} -> {file.url}')
            else:
                log.info(f'Other file: {file.src_path} -> {file.url}')
        # log.info(nav)
        # log.info(config)
        # log.info(files)
        return 'Hello World'
