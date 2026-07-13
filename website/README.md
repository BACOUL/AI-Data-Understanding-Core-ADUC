# ADUC Public Website

The first ADUC public website is a static, English-only site.

## Pages

- `index.html` — public homepage;
- `specification.html` — Core draft summary;
- `architecture.html` — project and standards architecture;
- `roadmap.html` — official phased roadmap;
- `example.html` — complete full-Core river example;
- `docs.html` — current “Try in 5 minutes” commands.

## Local preview

From the repository root:

```bash
python -m http.server 8000 --directory website
```

Then open:

```text
http://localhost:8000
```

## GitHub Pages deployment

`.github/workflows/deploy-pages.yml` publishes the `website/` directory when changes are merged to `main`.

The expected provisional URL is:

```text
https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/
```

The repository Pages source may need to be set to **GitHub Actions** once in repository settings. The workflow itself does not register a custom domain.

## Public-content rules

The website must always:

- state that ADUC is a working name;
- state that the specification is experimental;
- avoid calling ADUC a recognized standard;
- distinguish the full-Core vision from the currently implemented semantic-mapping subset;
- avoid claiming multi-model interoperability before qualifying external runs exist;
- remain usable without a commercial hosted service;
- remain English-only until the initial public terminology is stable.

## Domain policy

Do not buy, publish, or hard-code a custom ADUC domain until naming and trademark checks are complete. When a final domain is accepted, update:

- canonical metadata in every HTML page;
- `robots.txt`;
- `sitemap.xml`;
- deployment documentation.
