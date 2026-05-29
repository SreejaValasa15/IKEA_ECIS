from playwright.sync_api import expect
import re

class EcisDashboardPage:
    def __init__(self, page):
        self.page = page
        self.order_maintenance = page.get_by_role("link", name="Order Maintenance")
        self.menu_file = page.get_by_role("link", name="File")
        self.menu_maintenance = page.get_by_role("link", name="Maintenance")
        self.create_vmr_proposal = page.get_by_role("link", name="Create VMR Proposal")
        self.view_vmr_proposal = page.get_by_role( "link", name="View VMR Proposal")
        self.menu_reports = page.get_by_role("link", name="Reports")
        self.menu_supplier = page.locator("li a:has-text('Supplier')")
        self.submenu_user_pref = page.locator("a:has-text('User Preferences')")

    def update_user_preferences(self):
        self.page.wait_for_timeout(2000)
        self.menu_supplier.first.hover()
        self.submenu_user_pref.click()
        self.page.wait_for_timeout(2000)
        self.page.locator("#tabUser").click()
        self.page.wait_for_timeout(2000)
        self.page.locator("#rdbUserSearch").click()
        self.page.wait_for_timeout(2000)
        self.page.locator("#btnSave").click()
    def dashboard_page(self):
        expect(self.order_maintenance).to_be_visible(timeout=10000)

    def click_menu_file(self):
        expect(self.menu_file).to_be_visible(timeout=10000)
        self.menu_file.hover()

    def click_maintenance(self):
        expect(self.menu_maintenance.first).to_be_visible(timeout=10000)
        self.menu_maintenance.first.hover()

    def click_reports(self):
        expect(self.menu_reports).to_be_visible(timeout=10000)
        self.menu_reports.first.hover()

    def select_view_vmr_proposal(self):
            expect(self.menu_file).to_be_visible(timeout=10000)
            self.menu_file.click()
            self.page.wait_for_timeout(500)
            expect(self.view_vmr_proposal).to_be_attached(timeout=10000)
            self.view_vmr_proposal.click()
            self.page.wait_for_load_state("networkidle", timeout=15000)
            expect(self.page).to_have_url(
                re.compile(r"VMROrderProposals\.aspx"),
                timeout=10000
            )



