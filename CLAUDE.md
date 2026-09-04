# CLAUDE.md — MealWise

## Repo hygiene

- **Never add a `Co-Authored-By` trailer to commits.** No Claude/Anthropic co-authorship — the commits are mine, and the history was rewritten once already to strip them.
- Commit as `mohammadmassaf <mohammadmassaf1@gmail.com>` (already set repo-local).
- Commit often, small, imperative messages ("add USDA lookup cache", not "update").
- Never commit `.env`, API keys, `__pycache__`, `venv/`, or `node_modules/`. Rotate any leaked key immediately.
