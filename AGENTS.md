# NYCU Part-time Tester

pytest and Playwright scripts that log in to the NYCU portal with TOTP and sign in or out on the part-time system. `test_main.py` holds the flow and `scheduler.py` the schedule. Read [README.md](README.md) first.

## Rules

- Each test run signs the account in or out for real. Never run a test without the owner's request.
- Credentials come only from `.env`. Never print, log or commit `ACCOUNT`, `PASSWORD` or `TOTP`.
- Keep the `signin` and `signout` markers in `pyproject.toml` in agreement with the tests and the scheduler.
- Repository documents and code comments are English.

## Verify

```sh
uv sync
uv run python -c "import scheduler, test_main"
uv run pytest --collect-only -q
```

These commands do not touch the portal. A real run needs the owner's approval.
