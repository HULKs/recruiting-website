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
        'mkdocs.themes': [
            'recruiting_website = theme',
        ],
    },
    include_package_data=True,
)
