# VH3 AI: Docs source

This folder is the **source of truth** for the public Mintlify docs site
hosted at `docs.vh3.ai`.

## How publishing works

```
edit here  →  commit to main  →  .github/workflows/sync-docs.yml
                              →  mirrors to github.com/vh3-digital/docs
                              →  Mintlify auto-deploys
```

Only edit MDX/JSON/asset files **inside this `docs-site/` folder**. The
mirror repo (`vh3-ai/docs`) is auto-generated, never commit to it
directly, the next sync will overwrite it.

## Local preview

```bash
cd docs-site
npx mint dev
```

Opens the docs at `http://localhost:3000` with hot reload.

## Editorial rules (apply to every customer-facing page)

These rules are non-negotiable. Re-read before editing or adding MDX.

| Rule | Requirement |
|------|-------------|
| Locale | UK English (`organisation`, `licence`, `centre`, `-ise` verbs) |
| Punctuation | No em dashes (`—`). Use commas, full stops, colons, or parentheses |
| Tone | Plain, direct, earned claims. Written for people who run vans and contracts, not for a model card |
| Banned phrasing | Avoid: "leverage", "delve", "game-changer", "revolutionise", "unlock", "in today's landscape", "it's not X it's Y" stacked contrasts, "powerful AI", "simply ask" |
| Emojis | None in docs |
| Always-on language | The platform **runs 24/7**, is **always-on**, or **continuous**. Do not say "overnight" or "while you sleep" |
| Technology naming | Customer copy uses **intelligence layer**; name **n8n** where relevant; do not surface Neo4j, Weaviate, or model providers in operator pages |
| IDs in UI | Never instruct operators to use internal IDs in chat or screens; job refs and names only |

Quick checks before commit (run from repo root):

```bash
grep -rn "—" docs-site/         # em dashes
grep -rni "overnight\|while you sleep\|leverage\|delve" docs-site/
```

## Adding a page

1. Create the `.mdx` file in the appropriate subfolder (`api-reference/`,
   `guides/`, `agent-kits/`, etc.).
2. Add its slug to the relevant group in `docs.json` → `navigation.tabs`.
3. Add a `description` in the page frontmatter (used in `llms.txt` for AI discovery).
4. Commit and push to `main`. The sync workflow handles the rest.

## AI-friendly docs (Mintlify)

After deploy, Mintlify automatically serves:

| URL | Purpose |
|---|---|
| `https://docs.vh3.ai/llms.txt` | Page index for LLMs |
| `https://docs.vh3.ai/llms-full.txt` | Entire site as one Markdown file |
| `https://docs.vh3.ai/mcp` | Documentation search MCP (not the VH3 product API) |
| `https://docs.vh3.ai/<page>.md` | Markdown export per page |

Hosted skills live in `.mintlify/skills/` (e.g. `vh3-docs` for doc navigation).
Site-level AI settings are in `docs.json` (`description`, `contextual` menu).
Use `<Visibility for="agents">` in MDX for agent-only guidance that is hidden on the web UI.

## Required secrets (set in monorepo → Settings → Secrets and variables → Actions)

| Secret | Purpose |
|---|---|
| `DOCS_REPO_TOKEN` | Fine-grained PAT with `contents: write` on `vh3-digital/docs` |
