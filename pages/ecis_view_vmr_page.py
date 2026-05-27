from asyncio import wait

from playwright.sync_api import expect, Page
import allure
import re

from openpyxl import Workbook
from openpyxl import load_workbook
from pathlib import Path

class EcisViewVmrPage:
    def __init__(self, page):
        self.page = page
        self.view_vmr_proposal_link = page.get_by_role("link", name="View VMR Proposal")
        self.order_dropdown = page.locator("#OrderDropdowntxt")
        self.find_button = page.get_by_role("button", name="Find")
        self.search_filters = page.locator(".show_hide_span")
        self.order_checkboxes = page.locator("#grdOrderVmr_selectedRows")
        self.view_link = page.get_by_role("link", name="View")
        self.vmr_order_ref_label = page.locator("label", has_text="VMR Order Ref")
        self.vmr_art_no = page.locator("label", has_text="Art No")
        self.vmr_rcv_code = page.locator("label", has_text="Rcv Code")
        self.vmr_end_rcv = page.locator("label", has_text="End Rcv")
        self.vmr_status = page.locator("label", has_text="Status")
        self.slide_button = self.page.locator(".btn_slide")
        self.slide_active_button = self.page.locator(".btn_slide.active")
        self.panel = self.page.locator("#panel")
        self.ref_order_dropdown_button = self.page.locator("#OrderDropdown")
        self.vmr_order_ref_visible_inputs = self.panel.locator('input[type="text"]:visible')
        self.vmr_order_ref_dropdown = self.page.locator("#ddlOrder")
        self.rcv_code_filter_input = self.page.locator("#mltsel_ddlRcv")
        self.rcv_code_dropdown = self.page.locator("#btnddlRcv")
        self.rcv_code_rvc_dropdown = self.page.locator("#tblCombo_ddlRcv")
        self.end_rcv_filter_input = self.page.locator("#mltsel_ddlEndRcv")
        self.end_rcv_dropdown_button = self.page.locator("#btnddlEndRcv")
        self.art_no_filter_input = self.page.locator("#ArtNoDropdowntxt")
        self.art_no_dropdown = self.page.locator("#ArtNoDropdown")
        self.art_no_filter_input_value = self.page.locator("#mltsel_ddlArticle")
        self.art_no_rvc_dropdown = self.page.locator("#tblCombo_ddlArticle")
        self.status_filter_input = self.page.locator("#mltsel_ddlstatus")
        self.status_dropdown = self.page.locator("#btnddlstatus")
        self.find_btn = self.page.locator("#btnFind")
        self.header_locator = self.page.locator('#grdOrderVmr_headers th')
        self.view_button = self.page.locator('#lnkView')
        self.clear_button = page.get_by_role("button", name="Clear")
        self.receiver_dropdown = page.locator("#mltsel_ddlRcv")
        self.order_filter_dropdown = page.locator("#mltsel_ddlOrder")
        self.empty_cell = re.compile(r"^$")
        self.result_grid_rows = page.locator("table tbody tr")
        self.export_file_link = page.get_by_role("link", name="Export File")

    # ================= SCREENSHOT HELPERS =================

    def _screenshot_before(self, step_name: str):
        try:
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"BEFORE - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass

    def _screenshot_after(self, step_name: str):
        try:
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"AFTER - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass


    def view_vmr_proposal(self):
        self._screenshot_before("View VMR Proposal")
        self.view_vmr_proposal_link.click()
        self.page.wait_for_load_state("load", timeout=10000)
        self._screenshot_after("View VMR Proposal")

    def verify_search_filters_visible(self):
        self._screenshot_before("Verify Search Filters")
        if self.slide_button.is_visible():
            self.slide_button.click()
        self.page.wait_for_timeout(3000)
        if self.slide_active_button.is_visible():
            self.slide_active_button.click()
        expect(self.search_filters).to_be_visible(timeout=5000)
        self._screenshot_after("Verify Search Filters")

    def verify_search_options_available(self):
        self._screenshot_before("Verify Search Options")
        expect(self.vmr_order_ref_label).to_be_visible(timeout=5000)
        expect(self.vmr_art_no).to_be_visible(timeout=5000)
        expect(self.vmr_rcv_code).to_be_visible(timeout=5000)
        expect(self.vmr_end_rcv).to_be_visible(timeout=5000)
        expect(self.vmr_status).to_be_visible(timeout=5000)
        self._screenshot_after("Verify Search Options")

    def open_and_verify_vmr_order_ref_dropdown(self, *order_no):
        if not self.panel.is_visible():
            if self.slide_button.is_visible():
                self.slide_button.click()
            self.page.wait_for_timeout(1000)
            self.panel.wait_for(state="visible", timeout=5000)

        self.ref_order_dropdown_button.wait_for(state="visible", timeout=10000)
        self.ref_order_dropdown_button.click()
        self.page.wait_for_timeout(1000)

        # Use passed parameter if available, else fallback to default
        order_no = order_no[0] if order_no else "232310000001"

        found = False

        for i in range(self.vmr_order_ref_visible_inputs.count()):
            input_elem = self.vmr_order_ref_visible_inputs.nth(i)
            if input_elem.is_visible() and input_elem.is_enabled():
                input_elem.click()
                input_elem.press_sequentially(order_no, delay=100)
                expect(input_elem).to_have_value(order_no)
                found = True
                break

        if not found:
            raise Exception("No visible and enabled input found for VMR Order Ref after clicking dropdown.")

        self.vmr_order_ref_dropdown.wait_for(state="visible", timeout=5000)



    def open_and_verify_rcv_code_dropdown(self):
        self.rcv_code_filter_input.wait_for(state="visible", timeout=10000)
        self.rcv_code_filter_input.click()
        expect(self.rcv_code_dropdown).to_be_visible(timeout=3000)
        self.rcv_code_filter_input.press_sequentially("004 - STO", delay=100)
        self.page.wait_for_timeout(1500)  # Wait longer for dropdown to populate
        rows = self.rcv_code_rvc_dropdown.locator('tbody tr')
        row_count = rows.count()
        found = False
        visible_row_texts = []
        for i in range(row_count):
            row = rows.nth(i)
            if row.is_visible() and row.is_enabled():
                row_text = row.inner_text().strip()
                visible_row_texts.append(row_text)
                if "004 - STO" in row_text:
                    row.click()
                    found = True
                    break
        print(f"DEBUG: Visible RCV dropdown rows: {visible_row_texts}")
        if not found:
            raise Exception(f"No visible and enabled row containing '004 - STO' found in RCV dropdown. Rows: {visible_row_texts}")
        # Wait for the value to update after clicking
        try:
            expect(self.rcv_code_filter_input).to_have_value("004 - STO", timeout=3000)
        except AssertionError:
            # Try sending Enter if value did not update
            self.rcv_code_filter_input.press("Enter")
            self.page.wait_for_timeout(500)
            expect(self.rcv_code_filter_input).to_have_value("004 - STO", timeout=3000)

    def open_and_verify_end_rcv_dropdown(self):
        self.end_rcv_filter_input.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(500)
        self.end_rcv_dropdown_button.wait_for(state="visible", timeout=5000)
        self.end_rcv_dropdown_button.click()
        self.page.wait_for_timeout(500)
        self.end_rcv_filter_input.click()
        self.end_rcv_filter_input.fill("149 - STO")
        expect(self.end_rcv_filter_input).to_have_value("149 - STO")

    def open_and_verify_art_no_dropdown(self):
        self.art_no_filter_input.wait_for(state="attached", timeout=10000)
        expect(self.art_no_dropdown).to_be_visible(timeout=1000)
        self.art_no_filter_input.click()
        self.art_no_filter_input_value.press_sequentially("00038159", delay=100)

        self.page.wait_for_timeout(1500)  # Wait longer for dropdown to populate
        rows = self.art_no_rvc_dropdown.locator('tbody tr')
        row_count = rows.count()
        found = False
        visible_row_texts = []
        for i in range(row_count):
            row = rows.nth(i)
            if row.is_visible() and row.is_enabled():
                row_text = row.inner_text().strip()
                visible_row_texts.append(row_text)
                if "00038159" in row_text:
                    row.click()
                    found = True
                    break
        expect(self.art_no_filter_input_value).to_have_value("00038159", timeout=3000)

    def open_and_verify_status_dropdown(self):
        self.status_filter_input.wait_for(state="visible", timeout=10000)
        self.status_filter_input.click()
        expect(self.status_dropdown).to_be_visible(timeout=3000)


    def click_find(self):
        self._screenshot_before("Click Find")
        self.page.wait_for_timeout(1500)
        self.find_btn.click()
        self.page.wait_for_timeout(1500)
        self._screenshot_after("Click Find")

    def copy_clip_data_and_validate_copy_export(
            self,
            excel_path: str,
            csv_path: str
    ):
        expected_headers = [
            "VMR Order Reference", "Receiver Code","Receiver Type","End Receiver Code","End Receiver Type","Item ID",  "Item Quantity","Planned Dispatch Date","Creation Date","STATUS",
        ]
        self.copy_clip_data_and_save_to_files(
            excel_path=excel_path,
            csv_path=csv_path,
        )

    def copy_clip_data_and_save_to_files(
            self,
            excel_path: str,
            csv_path: str
    ):
        page = self.page
        page.locator("#grdOrderVmr_selectedRows").check()
        page.get_by_role("link", name="Copy Clip").click()
        frame = page.frame_locator("iframe")
        copy_clip_btn = frame.get_by_role("button", name="Copy to clipboard")
        expect(copy_clip_btn).to_be_attached(timeout=20000)
        copy_clip_btn.click()
        copy_data_btn = frame.get_by_role("button", name="Copy Data!")
        expect(copy_data_btn).to_be_attached(timeout=20000)
        copy_data_btn.click()
        clipboard_text = page.evaluate("navigator.clipboard.readText()")

        assert clipboard_text.strip(), "Clipboard data is empty"
        rows = [row.split("\t") for row in clipboard_text.splitlines()]
        excel_file = Path(excel_path)
        excel_file.parent.mkdir(parents=True, exist_ok=True)
        wb = Workbook()
        ws = wb.active
        ws.title = "Copied Data"

        for row in rows:
            ws.append(row)
        wb.save(excel_file)
        assert excel_file.exists(), "XLSX file was not created"
        csv_file = Path(csv_path)
        csv_file.parent.mkdir(parents=True, exist_ok=True)

        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            for row in rows:
                f.write(",".join(row) + "\n")

        assert csv_file.exists(), "CSV file was not created"

        self.page.mouse.click(5, 5)

    def verify_column_displayed(self):
        self._screenshot_before("Verify Columns")
        self.page.wait_for_timeout(1500)
        expected_columns = [
            "VMR Order Ref", "Rcv Code", "Rcv Type",
            "End Rcv Code", "End Rcv Type",
            "Art No", "Art Quantity",
            "Planned Dispatch Date", "Creation Date", "Status"
        ]
        actual = []
        for i in range(self.header_locator.count()):
            th = self.header_locator.nth(i)
            if th.is_visible():
                txt = th.inner_text().strip()
                if txt:
                    actual.append(txt)
        missing = [c for c in expected_columns if c not in actual]
        assert not missing, f"Missing columns: {missing}"
        self._screenshot_after("Verify Columns")


    def verify_view_button(self):
        expect(self.view_button).to_be_visible(timeout=5000)

    @allure.step("VMR Step 1: Open View VMR Proposal")
    def open_vmr_proposal(self):
        expect(self.view_vmr_proposal_link).to_be_visible(timeout=10000)
        self.view_vmr_proposal_link.click()

    @allure.step("VMR Step 2: Search for VMR Orders")
    def search_order(self):
        expect(self.order_dropdown).to_be_visible()
        self.order_dropdown.click()
        self.find_button.click()

    @allure.step("VMR Step 3: Select order and open details popup")
    def open_order_details_popup(self):
        # Select FIRST row checkbox safely
        expect(self.order_checkboxes.first).to_be_visible(timeout=10000)
        self.order_checkboxes.first.check()
        expect(self.order_checkboxes.first).to_be_checked()

        with self.page.expect_popup() as popup:
            self.view_link.click()

        return popup.value

    @allure.step("VMR Step 4: Validate order details in popup")
    def validate_order_popup_details(self, popup: Page):
        expect(popup.get_by_text("VMR Order Ref")).to_be_visible()

        popup.get_by_role("columnheader", name="Seq").click()
        popup.get_by_role("columnheader", name="Art No").click()
        popup.get_by_role("columnheader", name="Art Type").click()
        popup.get_by_role("columnheader", name="Art Quantity").click()


        popup.get_by_text("Planned Dispatch Date").click()
        popup.get_by_text("Sales Method").click()
        popup.get_by_text("DWP Number").click()
        popup.get_by_text("DWP Edition").click()
        popup.get_by_text("DWP From Date").click()

        popup.close()

    @allure.step("VMR Step 5: Clear search filters")
    def clear_search(self):
        self.page.wait_for_timeout(timeout=5000)
        self.clear_button.click()

    @allure.step("VMR Step 6: Apply receiver and order filters")
    def apply_receiver_and_order_filters(self):
        self.receiver_dropdown.click()
        self.page.get_by_role("cell").first.click()

        self.order_filter_dropdown.click()
        self.page.get_by_role("cell").filter(
            has_text=self.empty_cell
        ).click()

    @allure.step("VMR Step 1: Open View VMR Proposal")
    def open_vmr_proposal(self):
        expect(self.view_vmr_proposal_link).to_be_visible(timeout=10000)
        self.view_vmr_proposal_link.click()

    @allure.step("Apply VMR Order Ref filter and click Find")
    def apply_order_ref_filter(self, order_ref: str):

        expect(self.order_dropdown).to_be_enabled()
        self.order_dropdown.click()

        expect(self.order_filter_dropdown).to_be_visible()
        self.order_filter_dropdown.click()

        self.page.get_by_role("cell", name=order_ref, exact=True).click()

        expect(self.find_button).to_be_enabled()
        self.find_button.click()

    @allure.step("Verify VMR Order Ref appears in results")
    def verify_order_ref_in_results(self, order_ref: str):

        expect(
            self.page.get_by_role("gridcell", name=order_ref)
        ).to_be_visible(timeout=20000)

    @allure.step("Verify Sent Proposal status for Order Ref {order_ref}")
    def verify_sent_proposal_status_for_order(self, order_ref: str):
        # Locate the row containing the Order Ref
        row = self.page.get_by_role("row", name=order_ref)

        # Locate Sent Proposal status inside that row
        status_cell = row.get_by_role("gridcell", name="Sent Proposal")

        expect(status_cell).to_be_visible(timeout=20000)
        self.page.wait_for_timeout(timeout=5000)

    @allure.step("Verify Sent Proposal status for Order Ref {order_ref}")
    def verify_sent_proposal_status_for_order(self, order_ref: str):
        # Locate the row containing the Order Ref
        row = self.page.get_by_role("row", name=order_ref)

        # Locate Sent Proposal status inside that row
        status_cell = row.get_by_role("gridcell", name="Sent Proposal")

        expect(status_cell).to_be_visible(timeout=20000)

    @allure.step("Click Clear and reset filters")
    def clear_search(self):

        expect(self.clear_button).to_be_enabled()
        self.clear_button.click(timeout=10000)
        expect(self.order_filter_dropdown).to_be_visible(timeout=10000)

    def verify_result_grid_contains_expected_data(self, selected_vmr_ref: str):
        expect(self.result_grid_rows.first).to_be_attached(timeout=20000)

        rows = self.page.locator("table tbody tr")
        total_rows = rows.count()
        assert total_rows > 0, "No rows present in result grid"

        found = False

        for i in range(total_rows):
            row_text = rows.nth(i).inner_text()
            if selected_vmr_ref in row_text:
                found = True
                break

        assert found, f"Selected VMR Order Ref '{selected_vmr_ref}' not found in ANY grid row"
    @allure.step("Verify RCV and End RCV columns exist in result grid")
    def verify_rcv_columns_in_grid(self):
        headers = self.page.locator("table thead th")
        expect(headers.first).to_be_attached(timeout=20000)
        header_texts = [h.strip() for h in headers.all_inner_texts()]
        expected_columns = [
            "Rcv Code",
            "Rcv Type",
            "End Rcv Code",
            "End Rcv Type",
        ]
        for column in expected_columns:
            assert column in header_texts, (
                f"Column '{column}' not found in result grid headers"
            )


    # def export_vmr_order_proposal(self):
    #     self._screenshot_before("Export VMR Proposal")
    #     checkbox = self.page.locator("#grdOrderVmr_selectedRows")
    #     checkbox.wait_for(state="visible", timeout=20000)
    #     if not checkbox.is_checked():
    #         checkbox.check()
    #     self.export_file_link.wait_for(state="visible", timeout=20000)
    #     self.page.once("dialog", lambda d: d.accept())
    #     self.export_file_link.click()
    #     export_frame = self.page.frame_locator("iframe.cboxIframe")
    #     export_button = export_frame.locator("#btnExportToFile")
    #     export_button.wait_for(state="visible", timeout=20000)
    #     with self.page.expect_download(timeout=60000) as download_info:
    #         export_button.click()
    #     self._screenshot_after("Export VMR Proposal")
    #     self.page.mouse.click(5, 5)
    #     return download_info.value.suggested_filename
    def get_first_row_with_text(self):
        rows = self.page.locator("table tbody tr")
        self.page.wait_for_selector("table tbody tr", state="attached", timeout=20000)

        row_count = rows.count()

        for i in range(row_count):
            text = rows.nth(i).inner_text().strip()
            if text:
                return rows.nth(i)

        raise AssertionError("No populated row found in table")

    def export_vmr_order_proposal(self):
        row_checkbox = self.page.locator("#grdOrderVmr_selectedRows")
        row_checkbox.wait_for(state="visible", timeout=15000)

        if not row_checkbox.is_checked():
            row_checkbox.check()
        self.export_file_link.wait_for(state="visible", timeout=20000)
        # self.page.once("dialog", lambda d: d.accept())
        self.export_file_link.click()
        export_frame = self.page.frame_locator("iframe.cboxIframe")
        export_button = export_frame.locator("#btnExportToFile")
        export_button.wait_for(state="visible", timeout=20000)
        with self.page.expect_download(timeout=60000) as download_info:
            export_button.click()

        download = download_info.value
        return download.suggested_filename


    def _init_order_ref_container(self):
        if not hasattr(self, "_order_ref"):
            self._order_ref = {"value": None}

    def validate_vmr_order_reference(self):
        self._init_order_ref_container()

        assert self._order_ref["value"], (
            "VMR Order number was not captured from success dialog"
        )

    def handle_vmr_creation_dialog(self, dialog):
        self._init_order_ref_container()
        message = dialog.message
        match = re.search(r"\d+", message)
        if match:
            self._order_ref["value"] = match.group()

        dialog.accept()

    def create_order_total_pallet_and_verify(self):
        ref = {'value': None}

        def handle_dialog(dialog):
            alert_text = dialog.message
            ref['value'] = alert_text.split(":")[-1].strip()
            print(f"Dialog appeared with message: {alert_text}")
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.total_pallet.click()
        show_order_dropdown = self.page.locator('#mltsel_ddlVmiOrdNo')
        self.page.wait_for_selector('#mltsel_ddlVmiOrdNo', timeout=8000)
        expect(show_order_dropdown).to_have_value(ref['value'], timeout=5000)

        grid = self.page.locator("#grdVmiOrder tbody tr")
        try:
            self.page.wait_for_selector("#grdVmiOrder tbody tr", timeout=5000)
        except Exception:
            print("Grid row did not appear within timeout.")
        rows = grid.all()
        assert len(rows) == 1

    def verify_order_status_sent_proposal(self, selected_vmr_ref: str):
        self.page.evaluate("document.body.style.zoom='0.7'")
        self.page.wait_for_timeout(500)

        row = self.page.locator("table tbody tr", has_text=selected_vmr_ref).first
        expect(row).to_be_attached(timeout=15000)

