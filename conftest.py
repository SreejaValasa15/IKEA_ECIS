import pytest
from playwright.sync_api import sync_playwright, expect

import os
import json

from config.settings import BASE_URLS
from pages.ecis_dashboard_page import EcisDashboardPage
from pages.ecis_supplier_selection_page import EcisSupplierSelectionPage
from pages.ikea_login_page import IkeaLoginPage
from pages.ikea_welcome_page import IkeaWelcomePage
from pages.ecis_create_vmr_page import EcisCreateVmrPage
from pages.ecis_view_vmr_page import EcisViewVmrPage
from pages.ecis_order_maintenance_page import EcisOrderMaintenancePage
from pages.ecis_consignment_page import EcisConsignmentPage
from pages.ecis_order_maintenance_report_page import EcisOrderMaintenanceReportPage

@pytest.fixture(scope="function")
def ecis_dashboard_page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()

        # ---------- Step 1: Open URL ----------
        page.goto(BASE_URLS["url"])

        # ---------- Step 2: IKEA Welcome ----------
        ikea_welcome_page = IkeaWelcomePage(page)
        ikea_welcome_page.click_inter_button()

        # ---------- Step 3: IKEA Login ----------
        ikea_login_page = IkeaLoginPage(page)
        ikea_login_page.login(BASE_URLS["username"], BASE_URLS["password"])

        # ---------- Step 4: ECIS Welcome ----------
        ecis_welcome_page = EcisSupplierSelectionPage(page)

        try:
            ecis_welcome_page.database_dropdown.wait_for(state="visible")
        except Exception:
            try:
                # Handle session popup
                page.on("dialog", lambda dialog: dialog.accept())
                session_popup = page.locator("#serverSessionExpiryHeaderDiv")
                if session_popup.is_visible():
                    page.wait_for_load_state("networkidle", timeout=60000)
                    session_popup.locator("#Button2").click()
                    ikea_welcome_page.click_inter_button()
                    ikea_login_page.login(
                        BASE_URLS["username"],
                        BASE_URLS["password"]
                    )
                    page.wait_for_load_state("networkidle", timeout=60000)
            except Exception:
                page.wait_for_load_state("networkidle", timeout=60000)
                ikea_welcome_page.click_inter_button()
                ikea_login_page.login(BASE_URLS["username"], BASE_URLS["password"])
            page.wait_for_load_state("networkidle", timeout=60000)

        # ---------- Step 7: Dashboard ----------
        dashboard_page = EcisDashboardPage(page)
        create_vmr_page = EcisCreateVmrPage(page)
        view_vmr_page = EcisViewVmrPage(page)
        oder_maintenance_page = EcisOrderMaintenancePage(page)
        ecis_consignment_page = EcisConsignmentPage(page)
        ecis_order_report_page = EcisOrderMaintenanceReportPage(page)
        yield (
            ecis_welcome_page,
            dashboard_page,
            create_vmr_page,
            view_vmr_page,
            oder_maintenance_page,
            ecis_consignment_page,
            ecis_order_report_page,
        )
        ikea_login_page.logout_ecis()
        browser.close()
