<!-- 翻译自 README.md @ docs/readme-template-v2。只翻 "For AI agents" 以上的章节，英文版更新时一起改。 -->

<div align="center">

<h1>NYCU Part-time Tester</h1>

<p><strong>用 Playwright 测试定时在阳明交大兼任系统签到与签退。</strong></p>

[![Python](https://img.shields.io/badge/python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Playwright](https://img.shields.io/badge/Playwright-pytest-2EAD33?style=flat-square&logo=playwright&logoColor=white)](test_main.py)
[![License](https://img.shields.io/github/license/zyx1121/nycu-parttime-system-tester?style=flat-square)](LICENSE.md)

[English](README.md) | [繁體中文](README.zh-TW.md) | **简体中文**

</div>

阳明交大的兼任人员每个班次都要在 portal 签到与签退，漏按一次就少一份薪水。这个项目把这套流程写成 Playwright 测试：用你的账号与 TOTP 登录 NYCU portal，再按下签到或签退。调度器会在固定时间运行测试。

## 功能

- **签到签退写成测试**：`pytest -m signin` 与 `pytest -m signout`。
- **TOTP 登录**：测试从你的 TOTP URI 生成双因素验证码。
- **调度**：台北时间 08:00 与 13:00 签到，12:00 与 17:00 签退。

## 快速开始

```sh
uv sync
uv run playwright install
cp .env.example .env    # 再填入各个值
uv run pytest --headed -m signin
```

浏览器会打开、登录 portal 并帮你签到。

## 使用方式

```sh
uv run pytest --headed -m signin    # 签到
uv run pytest --headed -m signout   # 签退
uv run python scheduler.py          # 按调度运行
```

## 配置

| 变量 | 值 |
|------|----|
| `ACCOUNT` | NYCU portal 账号 |
| `PASSWORD` | NYCU portal 密码 |
| `TOTP` | TOTP URI，例如 `otpauth://totp/XXX?secret=BASE32SECRET` |

TOTP URI 的获取方式：解码 [NYCU Portal 双因素验证](https://portal.nycu.edu.tw/#/user/TwoFactorAuthentication)页面的 QR code。要改时间，编辑 `scheduler.py` 里的 job。

## 限制

- 测试按照 portal 页面编写，portal 改版可能会让它失效。
- `.env` 存有你的密码与 TOTP 密钥，请妥善保管。
- [nycu plugin](https://github.com/zyx1121/nycu) 提供给 agent 用的 `parttime_sign_in` 与 `parttime_sign_out` MCP 工具。

## 其他

给 AI agent 的结构化信息与开发说明在[英文版](README.md#for-ai-agents)。

## 许可证

[MIT](LICENSE.md)
