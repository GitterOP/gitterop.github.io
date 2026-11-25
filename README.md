# Juan David Cárdenas Z. — Academic website

Personal academic website built with Jekyll and a lightweight adaptation of Academic Pages. Content is in English, with a portrait and a persistent dark/light theme switch. It includes seven publications (one in Early Access), a downloadable CV, and short descriptions of three projects in progress.

## Run locally

Use Ruby 3.3 with development headers, a C/C++ compiler, and Bundler:

```bash
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

On this checkout, the equivalent helper also supports the locally prepared development environment:

```bash
ruby scripts/site.rb serve --host 127.0.0.1 --port 4000
```

Open [localhost:4000](http://127.0.0.1:4000). A production build and its checks are:

```bash
JEKYLL_ENV=production bundle exec jekyll build
python3 tests/check_site.py
```

See [quickstart.md](./quickstart.md) for content updates and GitHub Pages deployment. Template provenance is recorded in [THIRD_PARTY.md](./THIRD_PARTY.md).
