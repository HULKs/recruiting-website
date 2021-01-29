# HULKs Recruiting Website

This repository contains the code for the recruiting website of HULKs. It serves as an interactive learning platform for new HULK members and becoming members. The website is built with [MkDocs](https://mkdocs.org) and the *interactive-widgets* projects ([MkDocs plugin](https://github.com/h3ndrk/interactive-widgets-mkdocs/), [backend](https://github.com/h3ndrk/interactive-widgets-backend/)).

Pages are written in [Markdown](https://daringfireball.net/projects/markdown/) in the `docs/`-directory, see an [MkDocs guide on how to write pages](https://www.mkdocs.org/user-guide/writing-your-docs/).

Configuration settings for MkDocs are contained in `mkdocs.yml`, see the [MkDocs documentation about supported fields](https://www.mkdocs.org/user-guide/configuration/). The recruiting website uses a custom MkDocs theme (see the [MkDocs documentation about custom themes](https://www.mkdocs.org/user-guide/custom-themes/)) and some additional plugins to enable some features of the theme (e.g. navigation, page titles), see the [MkDocs documentation on how to write plugins](https://www.mkdocs.org/user-guide/plugins/).

[interactive-widgets-mkdocs](https://github.com/h3ndrk/interactive-widgets-mkdocs/) is used to convert custom HTML tags within the Markdown pages into interactive widgets (it generates custom HTML with JavaScript), but it does not come with styling for the widgets (therefore this repository contains the theme).

Since *interactive-widgets-mkdocs* does not build nor pull any Docker images, some images are built in this recruiting website repository, see the `docker/`-directory. In addition, the images of the [interactive-widgets-backend](https://github.com/h3ndrk/interactive-widgets-backend/) need to be built.

## Building

This section covers all necessary steps to build a complete and deployable website.

- Optional: Setup virtual environment for Python
- Install MkDocs and *interactive-widgets-mkdocs* plugin: `pip install git+https://github.com/h3ndrk/interactive-widgets-mkdocs.git`
- Install recruiting website packages: `pip install ./` (or `pip install --editable ./` for development)
- Build website with MkDocs: `mkdocs build`
- Ensure that the Docker images *interactive-widgets-backend* and *interactive-widgets-monitor* are present. If not, build them according to the [interactive-widgets-backend documentation](https://github.com/h3ndrk/interactive-widgets-backend/).
- Ensure that all Docker images referenced in the Markdown pages (e.g. in the `image` attributes of the HTML tags of the widgets) are present. If not, build them via running `docker-compose build` inside the `docker/`-directory.
- Optional: Adjust the configuration in the generated files in the `site/`-directory.
- In the `site/`-directory, start the website via `docker-compose up --build` (`--build` is optional but ensures that the static files are correctly built into a Docker container *interactive-widgets-nginx*).
- Connect to `http://localhost` to see the started page. (You may need to clear your cache.)

## License

MIT
