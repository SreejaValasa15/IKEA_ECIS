from playwright.sync_api import expect
from datetime import datetime
import allure
from openpyxl import Workbook
from pathlib import Path
import os


class EcisOrderMaintenancePage:
    BLOCKED_ORDER_MESSAGE = (
        "Selected Order line blocked due to deletion indicator - no action allowed!"
    )

    def __init__(self, page):
        self.page = page
        self.order_maintenance = page.locator("a[href = '../OrderMaintenance/OrderMaintenance.aspx']")
        self.order_maintenance_header = page.locator("div.slide")
        self.order = page.locator("#OrderDropdowntxt")
        self.order_type = page.locator("#mltsel_ddltype")
        self.find_button = page.locator("#btnFind")
        self.grid_row = self.page.locator("#grdOrder")
        self.cancel_button = self.page.locator("#lnkCancel")
        self.confirm_button = self.page.locator("#lnkConfirm")
        self.move_button = page.locator("#lnkMove")
        self.change_button = page.locator("#lnkChange")

        self.deletion_indicator_dropdown = page.locator("#mltsel_ddlDelInd")
        self.first_order_checkbox = page.locator(
            "#grdOrder_selectedRows"
        ).first
        self.all_orders_radio = page.get_by_role(
            "radio", name="All Orders"
        )
        self.deletion_indicator_l = page.get_by_role(
            "cell", name="L"
        )
        self.cancelled_status_cell = page.get_by_role(
            "gridcell", name="Cancelled"
        ).first
        self.delivery_status_s = page.get_by_role("cell", name="S")
        # --------------------
        self.visible_rows = page.locator("table tbody tr:visible")
        # Export locators
        self.export_button = page.locator("#btnExportFile")
        self.export_popup_export_btn = page.locator("#btnExportToFile")
        self.export_iframe = self.page.frame_locator("iframe")
        # CopyClip locators
        self.copy_clip_button = page.locator("#btnCopyClip")
        self.copyclip_frame = page.frame_locator("iframe")
        self.btn_copy_to_clipboard = self.copyclip_frame.locator("#btnCopyToClip")
        self.btn_copy_data = self.copyclip_frame.get_by_role(
            "button", name="Copy Data!"
        )
        self.copy_success_text = self.copyclip_frame.get_by_text(
            "Data Copied Successfully"
        )

    def click_order_link(self):
        self.order_maintenance.first.click()

    def verify_order_maintenance_header(self):
        self.page.wait_for_timeout(2000)
        expect(self.order_maintenance_header.first).to_have_text("Order Maintenance - Search", timeout=10000)

    def select_order_type(self, o_type):
        self.page.wait_for_timeout(2000)
        self.order_type.click()
        self.order_type.press_sequentially(o_type, delay=100)
        expect(self.order_type).to_have_value(o_type, timeout=5000)

    def click_find_button(self):
        self.find_button.click()
        self.page.wait_for_timeout(3000)

    def select_order_from_grid(self, order_number):
        self.grid_row.wait_for(state="visible", timeout=10000)

        # Get all rows from the grid
        row_grid = self.page.locator("#grdOrder tbody tr")

        # Get total number of rows
        row_count = row_grid.count()
        print(f"Total rows found: {row_count}")

        # Loop through each row
        for i in range(row_count):
            row = row_grid.nth(i)

            order_text = row.locator("td").nth(2).inner_text().strip()
            print(f"Row {i + 1} status: {order_text}")

            del_indicator = row.locator("td").nth(11).inner_text().strip()

            # If status is Pending, click the checkbox in first column
            if order_text == order_number and del_indicator == "":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break
        self.page.wait_for_timeout(10000)

    def verify_pending_status(self, order_number):
        # Get all rows from the grid
        row_grid = self.page.locator("#grdOrder tbody tr")

        # Get total number of rows
        row_count = row_grid.count()
        print(f"Total rows found: {row_count}")

        # Loop through each row
        for i in range(row_count):
            row = row_grid.nth(i)

            # Get the Status column text (2nd column, index = 1)
            status_text = row.locator("td").nth(1).inner_text().strip()

            order_text = row.locator("td").nth(2).inner_text().strip()

            # If status is Pending, click the checkbox in first column
            if order_text == order_number and status_text == "Pending":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break
            self.page.wait_for_timeout(10000)

    def click_move_button(self):
        with self.page.expect_popup() as popup_info:
            self.move_button.click()

        popup = popup_info.value

        # Validate popup URL
        expect(popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/OrderMaintenance/OrderMaintenanceMove.aspx"
        )
        plan_date = popup.locator("#newDate")
        today = datetime.today().strftime("%d-%m-%Y")
        plan_date.fill(today)

        move_btn = popup.locator("#btnMove")
        move_btn.click()

    def click_change_button(self):
        with self.page.expect_popup() as popup_info:
            self.change_button.click()

        popup = popup_info.value

        # Validate popup URL
        expect(popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/OrderMaintenance/OrderMaintenanceChange.aspx"
        )

        # Select first row checkbox
        row_grid = popup.locator("#grdOrderConfirm tbody tr").nth(0)
        checkbox = row_grid.locator("td").first.locator("input")
        checkbox.check()

        # Fill date
        plan_date = popup.locator("#newDate")
        today = datetime.today().strftime("%d-%m-%Y")
        plan_date.fill(today)

        # Click show change
        popup.locator("#btnShowChange").click()

        # Validate text
        expect(popup.locator("#divCapType")).to_have_text("Show DWP")

        # DWP selection
        actual_dwp = popup.locator("#mltsel_ddlDwpValidFrom")
        row_dwp_grid = popup.locator("#tblCombo_ddlDwpValidFrom tbody tr")
        change_dwp_btn = popup.locator("#divbtndwpsave")

        row_count = row_dwp_grid.count()
        print(f"Total rows found: {row_count}")

        for i in range(row_count):
            # Open dropdown
            actual_dwp.click()

            # Wait for rows
            row_dwp_grid.first.wait_for(state="visible")

            # Select option
            option = row_dwp_grid.nth(i)
            option_text = option.text_content()
            print(f"Trying option {i}: {option_text}")

            option.click()

            # Wait for UI update
            popup.wait_for_load_state("networkidle")

            # Check if button is enabled
            if change_dwp_btn.is_enabled():
                print(f"Button enabled for option: {option_text}")
                change_dwp_btn.click(force=True)
                break
            else:
                print(f"Button NOT enabled for option: {option_text}, trying next...")
    def click_cancel_button(self):
        with self.page.expect_popup() as popup_info:
            self.cancel_button.click()

        popup = popup_info.value
        # Validate popup URL
        expect(popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/OrderMaintenance/OrderMaintenanceCancel.aspx"
        )
        popup.wait_for_load_state("load")
        # Select all
        select_all_btn = popup.locator("#grdOrderConfirm_btnSelectAll")
        self.page.wait_for_timeout(2000)
        select_all_btn.click()

        cancel_btn = popup.locator("#btnCancel")
        expect(cancel_btn).to_be_visible(timeout=10_000)

        # ---------- FIRST DIALOG: No reason code ----------
        def handle_no_reason_dialog(dialog):
            assert dialog.message == "No Reason code filled in !"
            dialog.accept()  # OK

        popup.once("dialog", handle_no_reason_dialog)
        cancel_btn.click()

        # ---------- Select Reason ----------
        reason_ddl = popup.locator("#ReasonCodeDropdowntxt")
        expect(reason_ddl).to_be_visible(timeout=10_000)
        reason_ddl.click()

        row_reason = popup.locator("#tblCombo_ddlreasonCode tbody tr")
        row_reason.nth(1).click()

        # ---------- SECOND DIALOG: Confirmation ----------
        def handle_confirmation_dialog(dialog):
            assert "You are going to cancel" in dialog.message
            dialog.accept()  # OK

        popup.once("dialog", handle_confirmation_dialog)
        cancel_btn.click()

    def search_order_confirm(self, order_no):

        row_grid = self.page.locator("#grdOrder tbody tr")

        # Get total number of rows
        row_count = row_grid.count()
        print(f"Total rows found: {row_count}")

        # Loop through each row
        for i in range(row_count):
            row = row_grid.nth(i)

            order_text = row.locator("td").nth(2).inner_text().strip()
            print(f"Row {i + 1} status: {order_text}")

            del_indicator = row.locator("td").nth(11).inner_text().strip()

            # Get the Status column text (2nd column, index = 1)
            status_text = row.locator("td").nth(1).inner_text().strip()
            print(f"Row {i + 1} status: {status_text}")

            # If status is Pending, click the checkbox in first column
            if order_text == order_no and del_indicator == "" and status_text == "Pending":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break
            self.page.wait_for_timeout(1000)

    def click_confirm_button(self):
        with self.page.expect_popup() as popup_info:
            self.confirm_button.click()

        popup = popup_info.value
        confirm_btn = popup.locator("#btnConfirm")
        expect(confirm_btn).to_be_visible(timeout=10_000)
        confirm_btn.click()

    def change_supplier(self):
        self.page.wait_for_timeout(2000)
        self.page.locator("#btnchangesup").click()
        self.page.wait_for_timeout(2000)

    def select_delivery_status_s(self):
        expect(self.deletion_indicator_dropdown).to_be_enabled()
        self.deletion_indicator_dropdown.click()
        self.delivery_status_s.click()
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Selecting Deletion Indicator as S",
            attachment_type=allure.attachment_type.PNG
        )

    def select_first_order(self):
        expect(self.first_order_checkbox).to_be_visible(timeout=10000)
        self.first_order_checkbox.check()

    def click_confirm_and_validate_popup(self):
        self._click_and_validate_dialog(
            action_locator=self.confirm_button,
            action_name="Confirm"
        )
        self.page.mouse.click(5, 5)

    def click_move_and_validate_popup(self):
        self._click_and_validate_dialog(
            action_locator=self.move_button,
            action_name="Move"
        )
        self.page.mouse.click(5, 5)

    def click_change_and_validate_popup(self):
        self._click_and_validate_dialog(
            action_locator=self.change_button,
            action_name="Change"
        )
        self.page.mouse.click(5, 5)

    def _click_and_validate_dialog(self, action_locator, action_name):
        def dialog_handler(dialog):
            actual_message = dialog.message
            allure.attach(
                actual_message,
                name=f"{action_name} Popup Message",
                attachment_type=allure.attachment_type.TEXT
            )
            assert actual_message.strip() == self.BLOCKED_ORDER_MESSAGE, (
                f"\nExpected:\n{self.BLOCKED_ORDER_MESSAGE}\n\nActual:\n{actual_message}"
            )
            dialog.accept()
        self.page.once("dialog", dialog_handler)
        allure.attach(
            self.page.screenshot(full_page=True),
            name=f"{action_name} Link Visible",
            attachment_type=allure.attachment_type.PNG
        )
        action_locator.click()

    def select_all_orders(self):
        self.all_orders_radio.check()
        allure.attach(
            self.page.screenshot(full_page=True),
            name="All Orders Radio Button is clicked",
            attachment_type=allure.attachment_type.PNG
        )

    def select_deletion_indicator_l(self):
        self.deletion_indicator_dropdown.click()
        self.deletion_indicator_l.click()
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Deletion Indicator L is selected",
            attachment_type=allure.attachment_type.PNG
        )

    def validate_order_status_cancelled(self):
        self.cancelled_status_cell.wait_for(state="visible")
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Cancelled Status is Visible",
            attachment_type=allure.attachment_type.PNG
        )
        expect(self.cancelled_status_cell).to_have_text("Cancelled")


    EXPORT_DOWNLOAD_DIR = "downloads"

    def verify_export_order_maintenance_file(self):
        file_path = self.export_and_verify_file(
            download_dir=self.EXPORT_DOWNLOAD_DIR
        )
        self.page.wait_for_load_state("domcontentloaded")
        allure.attach(
            self.page.screenshot(full_page=True),
            name="After Export Order Maintenance",
            attachment_type=allure.attachment_type.PNG
        )
        self.page.mouse.click(5, 5)
        return file_path

    def export_and_verify_file(self, download_dir):
        def handle_dialog(dialog):
            assert "Create Export file" in dialog.message
            dialog.accept()
        self.page.once("dialog", handle_dialog)
        self.export_button.click()

        export_frame = self.page.frame_locator("iframe")
        with self.page.expect_download() as download_info:
            export_frame.get_by_role("button", name="Export").click()

        download = download_info.value
        assert download.suggested_filename
        assert download.suggested_filename.lower().endswith(".txt")

        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, download.suggested_filename)
        download.save_as(file_path)

        allure.attach(
            self.page.screenshot(full_page=True),
            name="After export file saved locally",
            attachment_type=allure.attachment_type.PNG
        )

        assert os.path.exists(file_path)
        assert os.path.getsize(file_path) > 0

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            assert content.strip()

        allure.attach(
            self.page.screenshot(full_page=True),
            name="Export file content validated",
            attachment_type=allure.attachment_type.PNG
        )

        self.page.wait_for_timeout(300)
        return file_path

    COPYCLIP_EXCEL_PATH = "test_copy_data_files/order_maintenance_copyclip.xlsx"
    COPYCLIP_CSV_PATH = "test_copy_data_files/order_maintenance_copyclip.csv"

    def verify_copyclip_and_save_data(self):
        excel_file, csv_file = self.copy_clip_data_and_save_to_files(
            excel_path=self.COPYCLIP_EXCEL_PATH,
            csv_path=self.COPYCLIP_CSV_PATH
        )
        self.page.wait_for_timeout(300)
        self.page.mouse.click(5, 5)
        return excel_file, csv_file

    def copy_clip_data_and_save_to_files(self, excel_path: str, csv_path: str):
        page = self.page
        frame = page.frame_locator("iframe")
        copy_clip_btn = page.locator("#btnCopyClip")
        expect(copy_clip_btn).to_be_attached(timeout=20000)
        page.once("dialog", lambda d: d.accept())
        copy_clip_btn.click()

        allure.attach(
            page.screenshot(full_page=True),
            name="After clicking CopyClip",
            attachment_type=allure.attachment_type.PNG
        )

        copy_to_clip_btn = frame.locator("#btnCopyToClip")
        expect(copy_to_clip_btn).to_be_attached(timeout=20000)

        page.once("dialog", lambda d: d.accept())
        copy_to_clip_btn.click()

        copy_data_btn = frame.get_by_role("button", name="Copy Data!")
        expect(copy_data_btn).to_be_attached(timeout=20000)
        copy_data_btn.click()

        success_text = frame.get_by_text("Data Copied Successfully")
        expect(success_text).to_be_visible(timeout=10000)

        allure.attach(
            page.screenshot(full_page=True),
            name="Data Copied Successfully message",
            attachment_type=allure.attachment_type.PNG
        )

        clipboard_text = page.evaluate("navigator.clipboard.readText()")
        assert clipboard_text.strip()

        allure.attach(
            page.screenshot(full_page=True),
            name="Clipboard data captured",
            attachment_type=allure.attachment_type.PNG
        )

        rows = [row.split("\t") for row in clipboard_text.splitlines()]
        excel_file = Path(excel_path)
        excel_file.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Copied Data"
        for row in rows:
            ws.append(row)
        wb.save(excel_file)

        csv_file = Path(csv_path)
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            for row in rows:
                f.write(",".join(row) + "\n")

        self.validate_copyclip_csv_data(csv_path=str(csv_file))

        return str(excel_file), str(csv_file)

    def validate_copyclip_csv_data(self, csv_path: str):
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Before validating CopyClip CSV file",
            attachment_type=allure.attachment_type.PNG
        )

        with open(csv_path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n").split(",") for line in f.readlines()]

        actual_headers = lines[0]
        data_rows = lines[1:]
        first_data_row = data_rows[0]

        allure.attach(
            self.page.screenshot(full_page=True),
            name="CopyClip CSV validation completed successfully",
            attachment_type=allure.attachment_type.PNG
        )