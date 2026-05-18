import allure
from allure_commons.types import AttachmentType

class EcisOrderMaintenanceReportPage:
    def __init__(self, page):
        self.page = page
        self.order_reports = page.get_by_role("link", name="Order")
        self.find_btn = page.locator("#btnExecuteQry")
        self.clear_column_btn = page.locator("#btnResetQry")
        self.column_selection_btn = page.locator("#btnSearchCriteria")
        self.dll_main = page.locator("#ddlMain")
        self.dll_reference = page.locator("#ddlReference")
        self.ddl_cus_info = page.locator("#ddlCsmInfo")
        self.customer_infor = page.locator("#ddlCustomerInfo")
        self.ddl_date = page.locator("#ddlDate")
        self.maintain_queries = page.locator("#btnLoadQry")

    def navigate_to_order_reports(self):
        self.page.wait_for_timeout(2000)
        self.order_reports.first.click()
        self.page.wait_for_timeout(5000)


    def click_on_order_report(self):
        self.screenshot_before(self.page, "Order Report")
        self.find_btn.click()
        self.page.wait_for_timeout(5000)
        self.screenshot_after(self.page, "Order Details")

    def click_on_clear_button(self):
        self.screenshot_before(self.page, "Clear Column")
        self.clear_column_btn.click()
        self.screenshot_after(self.page, "Clear Column")
        self.page.wait_for_timeout(5000)

    def click_column_selection_button(self):
        # self.screenshot_before(self.page, "Column Selection")
        self.page.evaluate("document.body.style.zoom = '70%'")
        # self.column_selection_btn.click()
        self.page.wait_for_timeout(2000)
        self.screenshot_after(self.page, "Column Selection")
        # self.page.wait_for_timeout(10000)

    def select_option_by_text(self, select_option, option_text):
        self.page.wait_for_timeout(2000)
        # For native <select>, you can use select_option, but for custom dropdowns or clickable <option> elements:
        if select_option == "Main":
            options = self.dll_main.locator("option")
            count = options.count()
            for i in range(count):
                text = options.nth(i).text_content()
                if text == option_text:
                    options.nth(i).click()
                    break
        elif select_option == "Reference":
            options = self.dll_reference.locator("option")
            count = options.count()
            for i in range(count):
                text = options.nth(i).text_content()
                if text == option_text:
                    options.nth(i).click()
                    break
        elif select_option == "Customer Info":
            options = self.customer_infor.locator("option")
            count = options.count()
            for i in range(count):
                text = options.nth(i).text_content()
                if text == option_text:
                    options.nth(i).click()
                    break
        elif select_option == "Date":
            options = self.ddl_date.locator("option")
            count = options.count()
            for i in range(count):
                text = options.nth(i).text_content()
                if text == option_text:
                    options.nth(i).click()
                    break
        self.screenshot_after(self.page, "Generate New Query")
    def click_on_find_button(self):
        self.screenshot_before(self.page, "Find Button")
        self.find_btn.click()
        self.page.wait_for_timeout(2000)
        self.screenshot_after(self.page, "Find Button")
    def generate_new_query(self):
        self.screenshot_before(self.page, "Generate New Query")
        self.select_option_by_text(self.dll_main, "Ord Status")
        self.select_option_by_text(self.dll_reference, "Order No 2")
        # self.select_option_by_text(self.ddl_cus_info, "Shipment Id")
        self.select_option_by_text(self.customer_infor, "Customer Name")
        self.select_option_by_text(self.ddl_date, "Rcv Date")
        self.find_btn.click()
        self.page.wait_for_timeout(20000)
        self.screenshot_after(self.page, "Generate New Query")


    def click_on_maintain_queries_button(self, file_name):
        self.screenshot_before(self.page, "Main Queries")
        self.maintain_queries.click()
        self.page.wait_for_timeout(5000)
        iframe_locator = self.page.frame_locator('iframe[src*="MaintainQuery.aspx"]')
        iframe_locator.locator("#txtNewQryName").fill(file_name)

        # Set up alert handler
        def handle_dialog(dialog):
            dialog.accept()
        self.page.on("dialog", handle_dialog)

        # Remove pointer events from <html> in iframe and click the button via JS
        self.page.evaluate('''
            var iframe = document.querySelector('iframe[src*="MaintainQuery.aspx"]');
            if (iframe && iframe.contentWindow) {
                var doc = iframe.contentWindow.document;
                var html = doc.querySelector('html');
                if (html) html.style.pointerEvents = 'none';
                var btn = doc.querySelector('#btnNew');
                if (btn) btn.click();
            }
        ''')
        self.page.wait_for_timeout(2000)
        self.screenshot_before(self.page, "Save Queries")
        self.page.evaluate(
            '''(file_name) => {
                var iframe = document.querySelector('iframe[src*="MaintainQuery.aspx"]');
                if (iframe && iframe.contentWindow) {
                    var doc = iframe.contentWindow.document;

                    var html = doc.querySelector('html');
                    if (html) html.style.pointerEvents = 'none';

                    var select = doc.querySelector("#lstQry");
                    if (select) {
                        var options = select.options;

                        for (var i = 0; i < options.length; i++) {
                            var text = options[i].textContent || options[i].innerText;

                            if (text && text.trim() === file_name) {
                                select.selectedIndex = i;
                                options[i].selected = true;

                                select.dispatchEvent(new Event('change', { bubbles: true }));

                                if (options[i].click) options[i].click();
                                break;
                            }
                        }
                    }
                }
            }''',
            file_name
        )
        self.screenshot_before(self.page, "Select Queries")
        self.page.evaluate('''
                  var iframe = document.querySelector('iframe[src*="MaintainQuery.aspx"]');
                  if (iframe && iframe.contentWindow) {
                      var doc = iframe.contentWindow.document;
                      var html = doc.querySelector('html');
                      if (html) html.style.pointerEvents = 'none';
                      var btn = doc.querySelector('#btnLoad');
                      if (btn) btn.click();
                  }
              ''')
        self.page.wait_for_timeout(2000)
        self.screenshot_after(self.page, "New Query Selection")
    def screenshot_before(self, page, step_name: str):
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"BEFORE - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass

    def screenshot_after(self, page, step_name: str):
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"AFTER - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass
