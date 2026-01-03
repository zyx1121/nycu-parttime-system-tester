import os
import time
import pytest

from playwright.sync_api import Page, expect
from dotenv import load_dotenv

from totp import totp


def load_env():

    load_dotenv()

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


def open_timeclock_parttime_popup(page: Page) -> Page:

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

    tc_page = open_timeclock_parttime_popup(page)

    signin(tc_page)

    time.sleep(10)


@pytest.mark.signout
def test_signout(page: Page):

    account, password, totp_uri = load_env()

    login_portal(page, account, password, totp_uri)

    tc_page = open_timeclock_parttime_popup(page)

    signout(tc_page)

    time.sleep(10)
