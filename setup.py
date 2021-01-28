import setuptools


setuptools.setup(
    name='mkdocs-recruiting-website',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=[
        'interactive_widgets_mkdocs',
        'mkdocs>=1.1.2',
    ],
    entry_points={
        'mkdocs.plugins': [
            'recruiting_website_navigation = recruiting_website.navigation.navigation:Plugin',
        ],
        'mkdocs.themes': [
            'recruiting_website = recruiting_website.theme',
        ],
    },
    include_package_data=True,
)
