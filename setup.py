import setuptools


setuptools.setup(
    name='mkdocs-recruiting-website',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'interactive_widgets_mkdocs',
        'mkdocs>=1.1.2',
    ],
    entry_points={
        'mkdocs.plugins': [
            'recruiting_website_navigation = recruiting_website.navigation.navigation:Plugin',
            'recruiting_website_title_remover = recruiting_website.title_remover.title_remover:Plugin',
        ],
        'mkdocs.themes': [
            'recruiting_website = recruiting_website.theme',
        ],
    },
    include_package_data=True,
)
