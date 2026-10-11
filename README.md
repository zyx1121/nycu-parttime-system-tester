<div align="center">

<h1>NYCU Part-time Tester</h1>

<p><strong>Playwright tests that sign in and sign out on the NYCU part-time system, on a schedule.</strong></p>

[![Python](https://img.shields.io/badge/python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Playwright](https://img.shields.io/badge/Playwright-pytest-2EAD33?style=flat-square&logo=playwright&logoColor=white)](test_main.py)
[![License](https://img.shields.io/github/license/zyx1121/nycu-parttime-system-tester?style=flat-square)](LICENSE.md)

**English** | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

</div>

Part-time staff at NYCU sign in and out on the portal for each shift. A missed click costs pay. This project runs that flow as Playwright tests: it logs in to the NYCU portal with your account and TOTP, then clicks sign in or sign out. A scheduler runs the tests at fixed times.

## Features

- **Sign in and sign out as tests**: `pytest -m signin` and `pytest -m signout`.
- **TOTP login**: the tests make the two-factor code from your TOTP URI.
- **Schedule**: sign in at 08:00 and 13:00, sign out at 12:00 and 17:00, Asia/Taipei time.

## Quick start

```sh
uv sync
uv run playwright install
cp .env.example .env    # then fill in the values
uv run pytest --headed -m signin
```

A browser opens, logs in to the portal and signs you in.

## Usage

```sh
uv run pytest --headed -m signin    # sign in
uv run pytest --headed -m signout   # sign out
uv run python scheduler.py          # run on the schedule
```

## Configuration

| Variable | Value |
|----------|-------|
| `ACCOUNT` | NYCU portal account |
| `PASSWORD` | NYCU portal password |
| `TOTP` | TOTP URI, such as `otpauth://totp/XXX?secret=BASE32SECRET` |

To get the TOTP URI, decode the QR code from [NYCU Portal two-factor authentication](https://portal.nycu.edu.tw/#/user/TwoFactorAuthentication). To change the times, edit the jobs in `scheduler.py`.

## Limits

- The tests follow the portal pages, so a portal redesign can break them.
- The `.env` file holds your password and TOTP secret. Keep it private.
- The [nycu plugin](https://github.com/zyx1121/nycu) has `parttime_sign_in` and `parttime_sign_out` MCP tools for agents.

## For AI agents

Facts for coding agents and LLM tools. The rules for changing the code are in [AGENTS.md](AGENTS.md).

- **Summary**: pytest and Playwright scripts that log in to the NYCU portal with TOTP and sign in or out on the part-time system. An APScheduler runner runs them.
- **Type**: cli
- **Interfaces**: `pytest -m signin`, `pytest -m signout`, `python scheduler.py`
- **Install**: `uv sync && uv run playwright install`
- **Run**: `uv run pytest --headed -m signin`
- **Verify**: `uv run pytest -m signin` passes and the portal shows the sign-in
- **Config**: `.env` with `ACCOUNT`, `PASSWORD`, `TOTP`
- **Secrets**: `PASSWORD` and the `TOTP` secret, in `.env` only
- **Limits**: Python 3.13. Depends on the portal page layout. Each run signs in or out for real.

## Development

`test_main.py` holds the login and the 2 tests. `scheduler.py` holds the cron jobs. A test run has a real effect on your attendance record, so test changes with care.

## License

[MIT](LICENSE.md)
