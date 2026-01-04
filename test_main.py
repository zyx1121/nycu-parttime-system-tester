import base64
import datetime
import hashlib
import hmac
import os
import pathlib
import time
from urllib.parse import parse_qs, urlparse

import dotenv
import pytest
from playwright.sync_api import Page, expect


def save_screenshot(page: Page, name: str):

    pathlib.Path("artifacts").mkdir(exist_ok=True)
    date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=f"artifacts/{name}_{date}.png", full_page=True)


def totp(uri: str) -> str:
    """
    Input:  otpauth://totp/XXX?secret=BASE32SECRET
    Output: 6-digit TOTP (default: SHA1, 30s, 6 digits)
    """

    u = urlparse(uri.strip())
    if u.scheme != "otpauth" or u.netloc.lower() != "totp":
        raise ValueError("uri must be otpauth://totp/...")

    qs = parse_qs(u.query)
    secret = (qs.get("secret") or [None])[0]
    if not secret:
        raise ValueError("uri must have secret=...")

    # Base32 decode (allow missing '=', allow lowercase/spaces)
    s = secret.strip().replace(" ", "").upper()
    s += "=" * ((-len(s)) % 8)
    key = base64.b32decode(s, casefold=True)

    # TOTP: counter = floor(time / 30)
    counter = int(time.time()) // 30
    msg = counter.to_bytes(8, "big")

    # HOTP (RFC 4226) + dynamic truncation
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    dbc = (
        ((h[offset] & 0x7F) << 24)
        | (h[offset + 1] << 16)
        | (h[offset + 2] << 8)
        | (h[offset + 3])
    )

    code = dbc % 1_000_000
    return f"{code:06d}"


def load_env():

    dotenv.load_dotenv()

    account = os.getenv("ACCOUNT")
    password = os.getenv("PASSWORD")
    totp_uri = os.getenv("TOTP")

    if not account or not password or not totp_uri:
        raise RuntimeError("Missing env: ACCOUNT / PASSWORD / TOTP")

    return account, password, totp_uri


def login_portal(page: Page, account: str, password: str, totp_uri: str):

    page.goto("https://portal.nycu.edu.tw/", timeout=60000)

    page.locator("#account").fill(account)
    page.locator("#password").fill(password)

    login_btn = page.locator('button[data-test="login-button"]')
    expect(login_btn).to_be_visible(timeout=60000)
    expect(login_btn).to_be_enabled(timeout=60000)
    login_btn.click()

    dialog = page.locator('div[role="dialog"][aria-label="二階段驗證"]')
    expect(dialog).to_be_visible(timeout=60000)

    code = totp(totp_uri)
    dialog.locator("input.el-input__inner").first.fill(code)
    dialog.get_by_role("button", name="確定").click()

    expect(dialog).to_be_hidden(timeout=60000)


def open_parttime(page: Page) -> Page:

    page.locator("li.el-menu-item.subitem", has_text="陽明交通大學").click(
        timeout=60000
    )

    link = page.locator('a[href="#/redirect/timeclockParttime"]').first
    expect(link).to_be_visible(timeout=60000)

    with page.expect_popup() as p:
        link.click()
    popup = p.value

    popup.wait_for_load_state("domcontentloaded", timeout=60000)
    return popup


def signin(tc_page: Page):

    sign_link = tc_page.locator(
        "#ContentPlaceHolder1_GridView_attend_LinkButton_signIn_0"
    )
    expect(sign_link).to_be_visible(timeout=60000)

    with tc_page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
        sign_link.click()

    confirm_btn = tc_page.locator("#ContentPlaceHolder1_Button_attend")
    expect(confirm_btn).to_be_visible(timeout=60000)

    with tc_page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
        confirm_btn.click()

    tc_page.wait_for_load_state("domcontentloaded", timeout=60000)


def signout(tc_page: Page):

    sign_link = tc_page.locator(
        "#ContentPlaceHolder1_GridView_attend_LinkButton_signOut_0"
    )
    expect(sign_link).to_be_visible(timeout=60000)

    with tc_page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
        sign_link.click()

    confirm_btn = tc_page.locator("#ContentPlaceHolder1_Button_attend")
    expect(confirm_btn).to_be_visible(timeout=60000)

    with tc_page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
        confirm_btn.click()

    tc_page.wait_for_load_state("domcontentloaded", timeout=60000)


@pytest.mark.signin
def test_signin(page: Page):

    account, password, totp_uri = load_env()

    login_portal(page, account, password, totp_uri)

    parttime_page = open_parttime(page)

    signin(parttime_page)

    save_screenshot(parttime_page, "signin")


@pytest.mark.signout
def test_signout(page: Page):

    account, password, totp_uri = load_env()

    login_portal(page, account, password, totp_uri)

    parttime_page = open_parttime(page)

    signout(parttime_page)

    save_screenshot(parttime_page, "signout")
