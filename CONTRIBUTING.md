# Contributing to dota2-external-esp

Thanks for your interest in this educational external-cheat research project.

## Scope

This repo is a **read-only external overlay** for studying game memory layouts,
overlay rendering and offset-based ESP techniques. It is intended for offline
practice against local lobbies and for reverse-engineering education.

## Ground rules

- Do not submit working anti-cheat bypasses for live matchmaking.
- Keep PRs focused: one feature or offset update per PR.
- Update `offsets/offsets.json` when the Dota 2 client patches.
- Add or update tests in `tests/` for any new processor logic.

## Workflow

1. Fork and branch from `main` (`feat/hero-icon-cache`, `fix/offsets-7.39`, ...).
2. Run `pytest -q` before opening a PR.
3. Describe what memory structures or overlay behavior changed.

## Code style

- Python 3.11+, type hints on public functions.
- Keep workers stateless where possible; state lives in `state/`.
- Log via `utils/logger.py`, never `print()` in pipeline code.