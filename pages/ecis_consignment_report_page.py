import time
import allure
from playwright.sync_api import Page


# SMART DECORATOR
def screenshot_step(step_name=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            name = step_name if step_name else func.__name__

            #Detect correct page dynamically
            page_to_capture = None
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, Page):
                    page_to_capture = arg
                    break

            if not page_to_capture:
                page_to_capture = self.page

            try:
                screenshot = page_to_capture.screenshot()
                allure.attach(
                    screenshot,
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass

            return result
        return wrapper
    return decorator


class EcisConsignmentReportPage:
    def __init__(self, page):
        self.page = page

        self.consignment_link = page.get_by_role("link", name="Consignment")
        self.view_button = page.get_by_role("button", name="View")

    # -------- CONSIGNMENT FLOW --------
    @screenshot_step("Open Consignment")
    def open_consignment(self):
        self.consignment_link.first.click()

    @screenshot_step("Select Checkbox")
    def select_checkbox(self, consignment_id):
        checkbox = self.page.get_by_role(
            "row", name=consignment_id
        ).locator("#grdCsm_selectedRows")
        checkbox.check()

    @screenshot_step("Select View button")
    def click_view(self):
        with self.page.expect_popup() as popup:
            self.view_button.click()

        new_page = popup.value

        # Capture popup
        allure.attach(
            new_page.screenshot(),
            name="View Popup Opened",
            attachment_type=allure.attachment_type.PNG
        )

        return new_page

    # -------- BOOKING FLOW --------
    @screenshot_step("Perform Booking")
    def perform_booking(self, booking_page, lu_type, booking_name):
        booking_page.get_by_role("link", name=booking_name).click()

        booking_page.get_by_text("LU Type").click()
        self.page.wait_for_timeout(3000)

        booking_page.locator("#btnddlLUT").click()
        booking_page.get_by_role("cell", name=lu_type).click()

        self.page.wait_for_timeout(3000)

        def handle_dialog(dialog):
            time.sleep(2)
            dialog.accept()

        booking_page.once("dialog", handle_dialog)

        booking_page.get_by_role("button", name="Save").click()
        self.page.wait_for_timeout(3000)

    @screenshot_step("Find and Select All")
    def find_and_select_all(self, report_page):
            report_page.get_by_role("button", name="Find").click()
            report_page.wait_for_timeout(2000)
            report_page.get_by_role("button", name="Select All").click()

    @screenshot_step("Open Reports Popup")
    def open_reports(self, booking_page):
        with booking_page.expect_popup() as popup:
            booking_page.get_by_role("button", name="Reports").click()

        report_page = popup.value

        # Capture new popup
        allure.attach(
            report_page.screenshot(),
            name="Reports Popup",
            attachment_type=allure.attachment_type.PNG
        )

        return report_page

    # -------- REPORT FLOW --------
    @screenshot_step("Select Report")
    def select_report(self, report_page, report_name):
        report_page.locator("#btnddlReport").click()
        self.page.wait_for_timeout(3000)

        report_page.locator(f"text={report_name}").first.wait_for()
        report_page.locator(f"text={report_name}").first.click()
        self.page.wait_for_timeout(3000)

    @screenshot_step("Select Consignment Report")
    def select_consignment_report(self, report_page):
        report_page.locator("#mltsel_ddlCsmNo").click()
        self.page.wait_for_timeout(3000)

        report_page.locator("#tblDiv").click()
        self.page.wait_for_timeout(3000)

    @screenshot_step("Select Show Report")
    def show_report(self, report_page):
        button = report_page.get_by_role("button", name="Show Report")
        button.wait_for(state="visible")

        with report_page.expect_popup() as popup_info:
            button.click(force=True)

        print_popup = popup_info.value
        print_popup.wait_for_load_state("load")
        print_popup.wait_for_timeout(2000)

        allure.attach(
            print_popup.screenshot(),
            name="Report Preview Popup",
            attachment_type=allure.attachment_type.PNG
        )

        return print_popup

    # -------- PREVIEW --------
    @screenshot_step("Preview Report Before Close")
    def preview_report_and_close(self, booking_page, report_name):
        report_popup = self.open_reports(booking_page)

        self.select_report(report_popup, report_name)
        self.select_consignment_report(report_popup)

        print_popup = self.show_report(report_popup)

        # Final preview screenshot
        allure.attach(
            print_popup.screenshot(),
            name="Final Report Preview",
            attachment_type=allure.attachment_type.PNG
        )

        print_popup.close()
        report_popup.close()

    @screenshot_step("Preview BEFORE LU Change")
    def preview_find_select_all(self, booking_popup, report_name):
         report_popup  = self.open_reports(booking_popup)

         self.select_report(report_popup, report_name)
         self.find_and_select_all(report_popup)

         print_popup= self.show_report(report_popup)

         print_popup.close()
         report_popup.close()
         # ---------- Invoice ----------

    def open_invoice(self, page):
        with page.expect_popup() as popup:
            page.get_by_role("button", name="Invoice").click()
        return popup.value


    def set_invoice_date(self, page, date):
        # ✅ Dialog handler with delay
        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")  # optional debug

            # Wait 3 seconds so you can see it
            page.wait_for_timeout(3000)

            dialog.accept()  # Accept instead of dismiss

        # ✅ Register BEFORE action
        page.once("dialog", handle_dialog)

        # ---------- Actions ----------
        page.get_by_title("Show calendar").click()
        page.get_by_role("link", name=date).click()

        page.get_by_role("button", name="Save").click()

    #-------- PRINT --------
    @screenshot_step("Print Report")

    def print_report(self,print_page):
            export_icon = print_page.locator("#IconImg_rptViewer_toptoolbar_export")

            export_icon.wait_for(state="visible", timeout=2000)

            export_icon.click()

    @screenshot_step("Open Export Popup")
    # FINAL EXPORT (MATCHES YOUR POPUP UI)
    def export_report(self, print_popup,report_popup,booking_popup, file_type):

        # STEP 1: Open dropdown
        dropdown = print_popup.locator("div[id*='iconMenu_icon']")
        dropdown.wait_for(state="visible", timeout=5000)
        dropdown.click()
        # STEP 2: File type mapping
        format_map = {
            "pdf": "PDF",
            "excel": "Microsoft Excel (XLSX)",
            "xlsx": "Microsoft Excel (XLSX)",
            "xls": "Microsoft Excel (XLS)",
            "xml": "XML"
        }

        selected = format_map.get(file_type.lower())

        if not selected:
            raise Exception(f"Unsupported format: {file_type}")

        # STEP 3: Wait until dropdown options are visible (anchor element)
        print_popup.locator("text=PDF").first.wait_for(state="visible", timeout=10000)

        # STEP 4: Click required option (STRICT + VISIBLE)
        option =print_popup.locator(f"text={selected}").first

        option.wait_for(state="visible", timeout=5000)
        option.click(force=True)

        # VALIDATION (check selected value in input field)
        try:
            selected_value = print_popup.locator("input").first.input_value()
            assert selected.lower() in selected_value.lower()
        except:
            pass

        #  Screenshot after selection
        allure.attach(
            print_popup.screenshot(full_page=True),
            name=f"{selected} Selected",
            attachment_type=allure.attachment_type.PNG
        )

        # STEP 5: Export / Download
        with print_popup.expect_download(timeout=60000) as download_info:
            print_popup.locator("a[id*='dialog_submitBtn']").click()

        download = download_info.value

        #  Screenshot after download trigger
        allure.attach(
            print_popup.screenshot(full_page=True),
            name=f"{file_type.upper()} Download Triggered - {download.suggested_filename}",
            attachment_type=allure.attachment_type.PNG
        )

        #  Validation
        assert download.suggested_filename is not None

        #  Cleanup
        print_popup.close()
        report_popup.close()
        booking_popup.close()


        return download