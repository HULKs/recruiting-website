# HULKs Recruiting Website

This repository contains the code for the recruiting website of HULKs. It serves as an interactive learning platform for new HULK members and becoming members. The website is built with [MkDocs](https://mkdocs.org) and the *interactive-widgets* projects ([MkDocs plugin](https://github.com/h3ndrk/interactive-widgets-mkdocs/), [backend](https://github.com/h3ndrk/interactive-widgets-backend/)).

Pages are written in [Markdown](https://daringfireball.net/projects/markdown/) in the `docs/`-directory, see an [MkDocs guide on how to write pages](https://www.mkdocs.org/user-guide/writing-your-docs/).

Configuration settings for MkDocs are contained in `mkdocs.yml`, see the [MkDocs documentation about supported fields](https://www.mkdocs.org/user-guide/configuration/). The recruiting website uses a custom MkDocs theme (see the [MkDocs documentation about custom themes](https://www.mkdocs.org/user-guide/custom-themes/)) and some additional plugins to enable some features of the theme (e.g. navigation, page titles), see the [MkDocs documentation on how to write plugins](https://www.mkdocs.org/user-guide/plugins/).

[interactive-widgets-mkdocs](https://github.com/h3ndrk/interactive-widgets-mkdocs/) is used to convert custom HTML tags within the Markdown pages into interactive widgets (it generates custom HTML with JavaScript), but it does not come with styling for the widgets (therefore this repository contains the theme). See [interactive-widget-mkdocs for usage documentation of the custom HTML tags of widgets](https://github.com/h3ndrk/interactive-widgets-mkdocs/).

Since *interactive-widgets-mkdocs* does not build nor pull any Docker images, some images are built in this recruiting website repository, see the `docker/`-directory. In addition, the images of the [interactive-widgets-backend](https://github.com/h3ndrk/interactive-widgets-backend/) need to be built.

## Building

This section covers all necessary steps to build a complete and deployable website. Tested with Python 3.8.

The following steps are required for initial setup:

1. Optional: Setup virtual environment for Python
2. Install MkDocs and *interactive-widgets-mkdocs* plugin: `pip install git+https://github.com/h3ndrk/interactive-widgets-mkdocs.git`
3. Install recruiting website packages: `pip install ./` (or `pip install --editable ./` for development)
4. Build all required Docker images (`interactive-widgets-backend`, `interactive-widgets-monitor`, and your own) by running `docker-compose build` inside the `docker/`-directory.
5. Build website with MkDocs: `mkdocs build`
6. Optional: Adjust the configuration in the generated files in the `site/`-directory.
7. In the `site/`-directory, start the website via `docker-compose up --build` (`--build` is optional but ensures that the static files are correctly built into a Docker container *interactive-widgets-nginx*).
8. Connect to `http://localhost` to see the started page. (You may need to clear your cache. Quit with Ctrl+C.)

Once the recruiting website was successfully built once, use one of the following steps to rebuild:

- If a **new Docker image** is referenced in an HTML tag (via the `image`-attribute, see [interactive-widgets-mkdocs documentation](https://github.com/h3ndrk/interactive-widgets-mkdocs/)): rerun from step 4 (see above)
- If **files within the `docker/`-directory changed**: rerun from step 4 (see above)
- If **files in the `docs/`-directory changed**: quit any previously started page, then rerun from step 5 (see above)
- If **files in the `recruiting_website/`-directory changed** and executed step 3 without `--editable`: rerun from step 3 (step 4 can be skipped); when previously executed with `--editable`, changes in the `recruiting_website/`-directory are automatically applied (recommended for development).

Currently, the recruiting-website will not raise any error when Docker images are missing. If widgets are not behaving correctly, check that all referenced Docker images are built (see step 4 above).

## License

MIT
