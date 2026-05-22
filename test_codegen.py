import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ingka-icow-test.eu.auth0.com/u/login/identifier?state=hKFo2SBZXzNKeXQzUGZZTmplV200bWdVNGNoajJjbnlZRlFQRKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIFRFcjNjRGJ0Y1hVN29hLVpoUGFzMXZRaWptQUUyaXdoo2NpZNkgWjdBQm4xZ0RuTFZwdERFS2VlRElXMlVWMmo5Q1NQdmo")
    page.get_by_role("button", name="Inter IKEA, Non Ingka").click()
    page.get_by_role("textbox", name="User Account").click()
    page.get_by_role("textbox", name="User Account").fill("wewan")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("")
    page.locator("#footer").click()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("ecisTestuserRet#2027")
    page.get_by_role("button", name="Sign in").click()
    page.locator("#ddlSuppliers").select_option("n|n~22569")
    page.get_by_role("button", name="Continue...").click()
    page.get_by_text("Maintenance Order Order").click()
    page.get_by_role("link", name="Consignment").first.click()
    page.get_by_role("row", name="ECIS33489 2438-LSC NB-Beijing").locator("#grdCsm_selectedRows").check()
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="View").click()
    page1 = page1_info.value
    with page1.expect_popup() as page2_info:
        page1.get_by_role("button", name="Reports").click()
    page2 = page2_info.value
    page2.locator("#btnddlReport").click()
    page2.get_by_role("cell", name="Packing Label for DDC/COS").click()
    page2.get_by_role("button", name="Find").click()
    page2.get_by_role("button", name="Select All").click()
    with page2.expect_popup() as page3_info:
        page2.get_by_role("button", name="Show Report").click()
    page3 = page3_info.value
    page3.close()
    with page2.expect_popup() as page4_info:
        page2.get_by_role("button", name="Show Report").click()
    page4 = page4_info.value
    page4.get_by_role("button", name="Print this report").click()
    page4.get_by_title("Close Window").click()
    page4.close()
    page2.close()
    page1.get_by_role("link", name="Transport Booking").click()
    page1.locator("#btnddlLUT").click()
    page1.get_by_role("cell", name="1M").click()
    page1.once("dialog", lambda dialog: dialog.dismiss())
    page1.get_by_role("button", name="Save").click()
    page1.get_by_text("Add Order Add HM Change Select All Reports Book Trp Dispatch Invoice Refresh").click()
    with page1.expect_popup() as page5_info:
        page1.get_by_role("button", name="Reports").click()
    page5 = page5_info.value
    page5.locator("#btnddlReport").click()
    page5.get_by_role("cell", name="Packing Label for DDC/COS").click()
    page5.get_by_role("button", name="Find").click()
    page5.get_by_role("button", name="Select All").click()
    with page5.expect_popup() as page6_info:
        page5.get_by_role("button", name="Show Report").click()
    page6 = page6_info.value
    page6.get_by_role("button", name="Print this report").click()
    with page6.expect_download() as download_info:
        page6.get_by_role("button", name="Export", exact=True).click()
    download = download_info.value
    page6.close()
    page5.close()
    page1.close()
    page9.get_by_role("button", name="Export this report").click()
    page9.get_by_role("button", name="Click here to access options").click()
    page9.get_by_role("cell", name="PDF", exact=True).click()
    with page9.expect_download() as download2_info:
        page9.get_by_role("button", name="Export", exact=True).click()
    download2 = download2_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
