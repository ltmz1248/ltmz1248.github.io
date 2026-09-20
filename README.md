# Computational Lithography Notes

A personal technical notebook on machine learning, computational lithography, and inverse lithography. The website, navigation, biography, articles, and image captions are all in English.

## Content

The first entry, **From the Photomask to the Wafer**, begins the semiconductor lithography course notes. Its 1,007-word text, five figures, and consolidated source credits are preserved from the edited English manuscript.

The biography contains only the approved description of a PhD student and the research field. The design uses a blue Cortana background. The small `117` button in the footer reveals a HALO easter egg.

## Local preview

The generator uses Python's standard library and requires no additional packages.

```sh
python scripts/build_content.py
python -m http.server 8787 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8787/`.

## GitHub Pages

In the repository's **Settings → Pages**, select **GitHub Actions** as the publishing source. The workflow in `.github/workflows/pages.yml` builds and publishes the `dist` directory after each push to `main`. It can also be started from the Actions tab.

The workflow reads the correct base path from GitHub Pages. Both a user site at `username.github.io` and a project site under a repository path are supported. To build a project site locally:

```sh
python scripts/build_content.py --base-path /repository-name
```

Only `dist` is published. Course PDFs and local editorial material are not part of the deployment.

## Add a note

1. Add an English Markdown file to `content/`, using the first note's front matter and figure format.
2. Put its image files in `dist/assets/` and refer to them as `assets/...` in Markdown.
3. Run the generator and check the local preview.
4. Commit and push to `main`; GitHub Actions updates the website.

The current renderer supports paragraphs, links, emphasis, figures with captions, and a single source-credit block at the end. The notebook currently uses the course-note category and lithography topic labels.

GitHub's publishing workflow documentation: <https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>.
