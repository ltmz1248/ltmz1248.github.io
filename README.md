# Computational Lithography Notes

A personal technical notebook on machine learning, computational lithography, and inverse lithography. The website, navigation, biography, articles, and image captions are all in English.

## Content

The first entry, **From the Photomask to the Wafer**, begins the semiconductor lithography course notes. Its 1,007-word text, five figures, and consolidated source credits are preserved from the edited English manuscript.

The biography contains only the approved description of a PhD student and the research field. The supplied black background with a blue Cortana ring appears as a small decoration at the top right, leaving a compact, text-first layout. The small `117` button in the footer reveals a HALO easter egg.

## Local preview

The generator uses Python's standard library and requires no additional packages.

```sh
python scripts/build_content.py
python -m http.server 8787 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8787/`.

## Article likes

Visitors can like a note without signing in using the **Like** button with a small HALO-inspired energy sword. Its dark blue twin-blade outline lights up after a successful like, and the label changes to **Liked**. The homepage and article share the same per-article counter, stored by [CountAPI](https://countapi.mileshilliard.com/). Loading a page only reads the total; pressing Like increments it. No API key or account is required. The design change preserves existing likes and browser vote history.

The browser remembers a successful like in local storage and prevents repeat clicks, including across tabs where Web Locks are supported. Clearing browser storage or using another browser allows another like. If a submission loses its reply, it remains pending rather than automatically adding another like. This is a lightweight public counter, not a verified count of unique people: the service has public write endpoints, so deliberate manipulation is possible, and availability depends on the external service. A failed read displays an unavailable state instead of a made-up total.

Counter keys are derived from the site identity and article slug in the generator. Keep these stable to retain existing totals. The browser sends only the public counter key, without credentials or the referring page URL.

Run the like behavior checks with Node.js:

```sh
node --test tests/likes.test.mjs
```

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
