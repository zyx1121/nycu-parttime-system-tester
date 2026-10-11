<!-- 翻譯自 README.md @ docs/readme-template-v2。只翻 "For AI agents" 以上的章節，英文版更新時一起改。 -->

<div align="center">

<h1>NYCU Part-time Tester</h1>

<p><strong>用 Playwright 測試定時在陽明交大兼任系統簽到與簽退。</strong></p>

[![Python](https://img.shields.io/badge/python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Playwright](https://img.shields.io/badge/Playwright-pytest-2EAD33?style=flat-square&logo=playwright&logoColor=white)](test_main.py)
[![License](https://img.shields.io/github/license/zyx1121/nycu-parttime-system-tester?style=flat-square)](LICENSE.md)

[English](README.md) | **繁體中文** | [简体中文](README.zh-CN.md)

</div>

陽明交大的兼任人員每個班次都要在 portal 簽到與簽退，漏按一次就少一份薪水。這個專案把這套流程寫成 Playwright 測試：用你的帳號與 TOTP 登入 NYCU portal，再按下簽到或簽退。排程器會在固定時間執行測試。

## 功能

- **簽到簽退寫成測試**：`pytest -m signin` 與 `pytest -m signout`。
- **TOTP 登入**：測試從你的 TOTP URI 產生雙因素驗證碼。
- **排程**：台北時間 08:00 與 13:00 簽到，12:00 與 17:00 簽退。

## 快速開始

```sh
uv sync
uv run playwright install
cp .env.example .env    # 再填入各個值
uv run pytest --headed -m signin
```

瀏覽器會開啟、登入 portal 並幫你簽到。

## 使用方式

```sh
uv run pytest --headed -m signin    # 簽到
uv run pytest --headed -m signout   # 簽退
uv run python scheduler.py          # 依排程執行
```

## 設定

| 變數 | 值 |
|------|----|
| `ACCOUNT` | NYCU portal 帳號 |
| `PASSWORD` | NYCU portal 密碼 |
| `TOTP` | TOTP URI，例如 `otpauth://totp/XXX?secret=BASE32SECRET` |

TOTP URI 的取得方式：解碼 [NYCU Portal 雙因素驗證](https://portal.nycu.edu.tw/#/user/TwoFactorAuthentication)頁面的 QR code。要改時間，編輯 `scheduler.py` 裡的 job。

## 限制

- 測試依照 portal 頁面撰寫，portal 改版可能會讓它失效。
- `.env` 存有你的密碼與 TOTP 密鑰，請妥善保管。
- [nycu plugin](https://github.com/zyx1121/nycu) 提供給 agent 用的 `parttime_sign_in` 與 `parttime_sign_out` MCP 工具。

## 其他

給 AI agent 的結構化資訊與開發說明在[英文版](README.md#for-ai-agents)。

## 授權

[MIT](LICENSE.md)
