import bs4
import mkdocs


log = mkdocs.plugins.log.getChild('recruiting-website-title-remover')


class Plugin(mkdocs.plugins.BasePlugin):

    def on_page_content(self, html: str, page: mkdocs.structure.pages.Page, config: mkdocs.config.base.Config, files: mkdocs.structure.files.Files):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        potential_title = soup.contents[0]
        assert potential_title.name == 'h1'
        potential_title.extract()
        return soup.encode_contents(formatter='html5').decode()
