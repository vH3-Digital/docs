---
name: vh3-docs
description: >
  Navigate and search the VH3 AI documentation at docs.vh3.ai. Use when you need API
  endpoints, authentication, field names, agent starter kits, guides, or OpenAPI details —
  not when the user asks for live operational data from their tenant (use the VH3 product
  MCP and agent kits for that).
license: Proprietary
compatibility: Works with any MCP client or HTTP fetch. No API credentials required for read-only docs access.
metadata:
  author: VH3 AI
  version: "1.0"
---

# VH3 documentation

You are helping a developer or agent **learn the VH3 AI platform from published documentation**. You do not have access to the customer's live jobs, engineers, or sites unless a separate VH3 product MCP is connected.

## Discovery

| Resource | URL |
|---|---|
| Documentation index | `https://docs.vh3.ai/llms.txt` |
| Full site as Markdown | `https://docs.vh3.ai/llms-full.txt` |
| Any page as Markdown | Append `.md` to the page URL (e.g. `https://docs.vh3.ai/quickstart.md`) |
| Docs MCP server | `https://docs.vh3.ai/mcp` |
| OpenAPI spec | `https://docs.vh3.ai/openapi.json` |

Prefer the **docs MCP** (`search` and query filesystem tools) or `llms.txt` over guessing API behaviour.

## Docs MCP vs product MCP

- **Docs MCP** (`https://docs.vh3.ai/mcp`): searches this documentation site only. Use for "how do I call aggregate?", valid parameters, authentication, agent kits.
- **VH3 product MCP** (https://docs.vh3.ai/agent-kits/mcp-setup): live tenant data — jobs, sentinels, reports, investigate. Requires JWT from the customer's VH3 account. Not the same server as docs MCP.

## Where to look first

| Topic | URL |
|---|---|
| First API call | https://docs.vh3.ai/quickstart |
| `company_id` + `api_key` | https://docs.vh3.ai/authentication |
| Endpoint list | https://docs.vh3.ai/api-reference/overview |
| Coding agents in a repo | https://docs.vh3.ai/agent-kits/agents-md |
| Claude Code skills (ops) | https://docs.vh3.ai/agent-kits/claude-skills |
| Cursor rules | https://docs.vh3.ai/agent-kits/cursor-rules |
| Live data MCP setup | https://docs.vh3.ai/agent-kits/mcp-setup |

## Rules for agents

- Read documentation before inventing parameter names, metrics, or report types.
- Base URL for API calls: `https://api.vh3connect.io` (see `/authentication` for path prefixes).
- Never embed real `company_id` or `api_key` values from documentation examples into generated code; use placeholders or environment variables.
- Legacy v1 endpoints often use `company_id` / `api_key` (snake_case); v2 filters often use camelCase — check the OpenAPI spec when unsure.

## Install

```bash
npx skills add https://docs.vh3.ai
```
