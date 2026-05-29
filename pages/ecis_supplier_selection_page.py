import allure
class EcisSupplierSelectionPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#txtUserName")
        #class-> .  id->#
        self.database_dropdown = page.locator("#ddlDatabase")
        self.supplier_dropdown = page.locator("#ddlSuppliers")
        self.continue_button = page.locator("#btnContinue")

    def wait_for_database_dropdown(self, timeout=10000):
        self.database_dropdown.wait_for(state="visible", timeout=timeout)

    def select_database(self, value: str):
        self.wait_for_database_dropdown()
        self.database_dropdown.select_option(value=value)

    def select_supplier(self, value: str):
            self.supplier_dropdown.select_option(value=value)

    def click_continue(self):
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Supplier Selection",
            attachment_type=allure.attachment_type.PNG
        )
        self.continue_button.click()