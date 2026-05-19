from playwright.sync_api import expect

import allure
from allure_commons.types import AttachmentType
import os

class EcisOrderMaintenanceReportPage:
    def __init__(self, page):

        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

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

        self.reports_link = page.get_by_role("link", name="Reports")
        self.order_link = page.get_by_role("link", name="Order", exact=True)
        self.copy_clip_link = page.get_by_role("link", name="Copy Clip")
        self.close_button = page.get_by_role("button", name="close")
        self.print_link = page.get_by_role("link", name="Print")
        self.iframe = page.frame_locator("iframe")
        self.copy_to_clipboard_button = self.iframe.get_by_role("button", name="Copy to clipboard")
        self.copy_data_button = self.iframe.get_by_role("button", name="Copy Data!")

        self.order_report_link = page.locator("a[href='OrderReport.aspx']")
        # self.find_button = page.locator("#btnExecuteQry")
        self.export_file_button = page.locator("#btnPrintFile")
        self.rcv_dropdown = page.locator("#btnddlRcv")
        self.order_type_dropdown = page.locator("#btnddlOrderType")
        self.art_no_dropdown = page.locator("#btnddlArtNo")
        self.grid_rows = page.locator("#grdOrderReport tr")

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
    def go_to_reports(self):
        self.reports_link.click()
        # self.capture_screenshot("go_to_reports")

    def go_to_order(self):
        self.order_link.click()
        # self.capture_screenshot("go_to_order")

    def open_copy_clip(self):
        self.copy_clip_link.click()
        self.capture_screenshot("open_copy_clip")

    def interact_with_iframe(self):
        self.copy_to_clipboard_button.wait_for(state="visible")
        self.copy_to_clipboard_button.click()
        self.capture_screenshot("clicked_copy_to_clipboard")

        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")
            assert "Copying large number of records may take some time." in dialog.message
            dialog.accept()

        self.page.once("dialog", handle_dialog)

        self.copy_data_button.click()
        self.capture_screenshot("clicked_copy_data")

    def close_iframe(self):
        self.close_button.click()
        self.capture_screenshot("close_iframe")

    # ------- Print Section -------------------------

    def open_print_popup(self):
        with self.page.expect_popup() as popup_info:
            self.print_link.click()
            self.capture_screenshot("After clicking Report button")


        self.print_popup = popup_info.value

        # ✅ Popup locators
        self.print_report_button = self.print_popup.get_by_role(
            "button", name="Print this report"
        )
        self.export_button = self.print_popup.get_by_role(
            "button", name="Export", exact=True
        )

        self.export_btn = self.print_popup.get_by_role("button", name="Export this report")
        self.options_btn = self.print_popup.get_by_role("button", name="Click here to access options")

        self.pdf_option = self.print_popup.get_by_role("menuitem", name="PDF")
        self.excel_option = self.print_popup.get_by_role("menuitem", name="Microsoft Excel(XLS)")

        self.export_options = {
            "PDF": self.pdf_option,
            "Microsoft Excel(XLS)": self.excel_option
        }


    def print_report(self):
        self.print_report_button.click()
        self.attach_screenshot("After clicking Report button")

    def export_report(self):
        self.export_button.click()
        self.attach_screenshot("After clicking Export button")


    def export_pdf_report(self, export_type: str):
        self.export_btn.click()
        self.attach_screenshot("After clicking Export button")
        self.options_btn.click()
        self.attach_screenshot("After clicking Options button")


        self.export_options[export_type].click()
        self.attach_screenshot(f"{export_type} selected")

        with self.print_popup.expect_download() as download_info:
            self.export_button.click()

        return download_info.value

    # ✅ Cleanup
    def close_popup(self):
        if self.print_popup:
            self.print_popup.close()
            self.capture_screenshot("popup_closed")

    def capture_screenshot(self, step_name: str):
        file_path = f"{self.screenshot_dir}/{step_name}.png"
        self.page.screenshot(path=file_path)

        # ✅ Attach to Allure
        allure.attach.file(
            file_path,
            name=step_name,
            attachment_type=allure.attachment_type.PNG
        )

    def attach_screenshot(self, name: str):
        allure.attach(
            self.print_popup.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def navigate_to_order(self):
        reports_menu = self.page.locator("li:has-text('Reports')")
        reports_menu.hover()
        reports_menu.locator("a:has-text('Order')").filter(has_text="Order").first.click()

    def click_find_button(self):
        self.page.wait_for_timeout(500)
        self.screenshot_before(self.page, "Clicked File Button")
        self.find_btn.wait_for(state="visible", timeout=10000)
        self.find_btn.click()
        self.page.wait_for_timeout(500)
        self.screenshot_after(self.page, "Clicked Find Button")

    def handle_dialog(self):

        def dialog_handler(dialog):
            allure.attach(
                dialog.message,
                name="Dialog Message",
                attachment_type=allure.attachment_type.TEXT
            )
            dialog.accept()

        self.page.once("dialog", dialog_handler)

    def export_order_report_file(self):
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        self.export_file_button.wait_for(state="visible", timeout=20000)
        # self.page.once("dialog", lambda d: d.accept())
        self.handle_dialog()

        self.export_file_button.click()
        self.page.wait_for_timeout(500)

        self.screenshot_after(self.page, "Clicked Export File Button")
        export_frame = self.page.frame_locator("iframe.cboxIframe")
        export_frame.locator("#btnExportToFile").wait_for(state="visible", timeout=20000)
        # Locate Export button inside popup
        export_button = export_frame.locator("#btnExportToFile")
        export_button.wait_for(state="visible", timeout=20000)

        self.screenshot_before(self.page, "Before Popup Export Click")

        with self.page.expect_download(timeout=60000) as download_info:
            export_button.click(force=True)

            self.page.wait_for_timeout(500)

            self.screenshot_after(self.page, "Download Triggered")

        download = download_info.value

        #  Validate filename
        file_name = download.suggested_filename

        print(f"Downloaded file: {file_name}")

        allure.attach(
                file_name,
                name="File exported",
                attachment_type=allure.attachment_type.TEXT
            )

        assert file_name, " File name is empty"
        assert file_name.lower().endswith(".txt"), f" Unexpected file type: {file_name}"

        file_path = os.path.join(download_dir, file_name)
        download.save_as(file_path)

        assert os.path.exists(file_path), "File not found after download"
        assert os.path.getsize(file_path) > 0, "File is empty"

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            assert content.strip(), " File content is empty"

        self.screenshot_after(self.page, "File Validated Successfully")
        self.page.wait_for_timeout(2000)
        self.page.locator("#cboxClose").click(force=True)

        return file_path

    def get_cell_by_name(self, value):
        return self.page.get_by_role("cell", name=value)

    def select_rcv(self, value):

        self.screenshot_before(self.page, f"Before Select RCV - {value}")

        self.rcv_dropdown.click()
        self.get_cell_by_name(value).click()

        self.screenshot_after(self.page, f"After Select RCV - {value}")

    def select_order_type(self, value):

        self.screenshot_before(self.page, f"Before Select Order Type - {value}")

        self.order_type_dropdown.click()
        self.get_cell_by_name(value).click()

        self.screenshot_after(self.page, f"After Select Order Type - {value}")

    def select_art_no(self, value):

        self.screenshot_before(self.page, f"Before Select Art No - {value}")

        self.art_no_dropdown.click()
        self.get_cell_by_name(value).click()

        self.screenshot_after(self.page, f"After Select Art No - {value}")

    def search_order_report(self, data):

        self.screenshot_before(self.page, "Before Search Order Report")

        self.select_rcv(data["rcv"])
        self.click_find_button()
        self.page.wait_for_timeout(1000)

        self.select_order_type(data["order_type"])
        self.click_find_button()
        self.page.wait_for_timeout(1000)

        self.select_art_no(data["art_no"])
        self.click_find_button()
        self.page.wait_for_timeout(1000)

        self.screenshot_after(self.page, "After Search Order Report")


    def validate_search_results(self, retry=1):

        self.screenshot_before(self.page, "Before Validation")

        for attempt in range(retry + 1):

            self.page.wait_for_timeout(2000)

            count = self.grid_rows.count()

            if count > 0:
                expect(self.grid_rows.first).to_be_visible()

                self.screenshot_after(
                    self.page,
                    f"Validation Success - Rows Found: {count}"
                )
                return count

            if attempt < retry:
                self.click_find_button()

        allure.attach(
            "No data found after retries",
            name="Validation Failure",
            attachment_type=allure.attachment_type.TEXT
        )

        self.screenshot_after(self.page, "Validation Failed - No Data")

        assert False, "No data found in Order Report"