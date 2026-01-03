# NYCU Part-time Sign In/Out Tester

This is a test suite for the sign in and sign out flow of the NYCU part-time system.

## Environment Setup

1. Use `uv` to install the dependencies:

```bash
uv sync
```

2. Copy the `.env.example` file to `.env` and fill in the values:

```bash
cp .env.example .env
```

Example `.env.example`:

```env
ACCOUNT=your_account
PASSWORD=your_password
TOTP=otpauth://totp/XXX?secret=BASE32SECRET
```

> [!NOTE] The `TOTP` is the URI of the TOTP token, you can get it from [NYCU Portal / Two Factor Authentication](https://portal.nycu.edu.tw/#/user/TwoFactorAuthentication). using QR code decoder to get the URI.

## Usage

- Sign in:

```bash
uv run pytest --headed -m signin
```

- Sign out:

```bash
uv run pytest --headed -m signout
```

## License

MIT License. See [LICENSE.md](LICENSE.md) for details.
