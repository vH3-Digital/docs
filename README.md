# VH3 AI docs

Source for the public documentation site at [docs.vh3.ai](https://docs.vh3.ai).

## Local preview

```bash
cd docs-site
npx mint dev
```

Opens the docs at `http://localhost:3000` with hot reload.

## Structure

- `*.mdx` / `guides/` / `api-reference/` / `agent-kits/` — site pages
- `connect/` — VH3 Connect operator and admin how-tos
- `docs.json` — navigation and site config
- `openapi.json` — API reference schema
- `images/connect/` — approved Connect screenshots
- `.screenshot-staging/connect/` — raw captures (gitignored); see `SCREENSHOTS.md` there
