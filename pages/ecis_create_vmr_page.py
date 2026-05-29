from playwright.sync_api import expect
from pathlib import Path
import allure
import re
import os
import time
class EcisCreateVmrPage:
    EXCEL_FILE = Path("testdata/vmr56.xls")

    def __init__(self, page):
        self.page = page
        self.create_vmr_proposal_link = page.get_by_role("link", name="Create VMR Proposal")
        self.vmr_order_link = page.get_by_role("link", name="VMR Order")
        self.upload_radio = page.locator("#rdbVmrUploadOrder")
        self.vmr_order_upload_label = page.locator(
            "label", has_text="VMR order upload"
        )

        self.create_vmr = page.locator("#Views_0")
        self.receiver = page.locator("#mltsel_ddlVmiRcvCode")
        self.receiver_code = page.locator("#tblCombo_ddlVmiRcvCode")
        self.plan_date = page.locator("#datepicker")
        self.article_no_dropdown = page.locator("#btnddlVmiArtNo")
        self.article_no_list = page.locator("#tblCombo_ddlVmiArtNo")
        self.selected_article_no = page.locator("#mltsel_ddlVmiArtNo")
        self.proposed_qty = page.locator("#txtProposedQty")
        self.add_article = page.locator("#btnAdd")
        self.per_pallet = page.locator("#btnCreateOrderP")
        self.total_pallet = page.locator("#btnCreateOrderA")
        self.qty_unit_load = page.locator("#txtQtyUnitLoad")
        self.vmr_order_upload_radio = page.get_by_text("VMR Upload")
        self.vmr_order_proposal_upload_option = page.get_by_text("VMR Order Proposal Upload")
        self.download_template_option = page.locator("#rdbVmrDownload")
        self.upload_vmr_order_proposal_option = page.locator("#rdbVmrUploadOrder")
        self.upload_vmr_transit_order_proposal_option = page.locator("#rdbVmrUploadTransitOrder")
        self.download_file_button = page.locator("#btnDownloadTemplate")
        self.download_button = page.frame_locator(".cboxIframe").locator("#btnDownloadTemplate")
        self.choose_file_button = page.get_by_role("button", name="Choose File")
        self.start_upload_button = page.get_by_role("button", name="Start Upload")
        self.popup_close = page.frame_locator("#cboxClose")
        self.export_invalid_orders_button = page.locator("#btnExportToFile")
        # Excel test data path
        self.PROJECT_ROOT = Path(__file__).resolve().parents[1]
        self.EXCEL_FILE_RCV = self.PROJECT_ROOT / "testdata" / "vmr_same_rcv2.xls"
        self.EXCEL_FILE_PATH = self.PROJECT_ROOT / "testdata" / "vmr_diff_rcv2.xls"
        # self.find_button = page.get_by_role("button", name="Find")
        self.export_file_link = page.get_by_role("link", name="Export File")
        self.result_grid_rows = page.locator("table tbody tr")

    def select_vmr_order_upload(self):
        try:
            expect(self.vmr_order_upload_label).to_be_visible(timeout=10000)
            self.vmr_order_upload_label.click()
        except  Exception:
            self.vmr_order_upload_radio.click()

    def select_vmr_order_upload_label(self):
        expect(self.vmr_order_upload_label).to_be_visible(timeout=10000)
        self.vmr_order_upload_label.click()

    def select_download_and_confirm(self):
        self.download_template_option.click()

    def click_download_button(self):
        expect(self.download_file_button).to_be_visible()

        with self.page.expect_download() as download_info:
            self.download_file_button.click()
            self.page.wait_for_timeout(2000)
            self.download_button.click()
        download = download_info.value
        # Save the file as 'Upload_File' in the Downloads directory
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        download.save_as(os.path.join(download_dir, "Upload_File"))

    def verify_file_downloaded(self, filename="Upload_File"):
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(download_dir, filename)
        # Wait up to 10 seconds for file to appear
        for _ in range(20):
            if os.path.exists(file_path):
                return True
            time.sleep(0.5)
        assert False, f"File {filename} was not downloaded to {download_dir}"

    def close_download_popup(self):
        self.page.wait_for_selector("#cboxClose", timeout=10000)
        self.page.locator("#cboxClose").click(force=True)
        self.page.wait_for_selector(
            "#cboxOverlay",
            state="hidden",
            timeout=10000,
        )
        self.page.wait_for_timeout(500)

    def create_vmr_proposal(self):
        self.create_vmr_proposal_link.click()
        self.page.wait_for_load_state("load", timeout=10000)
        expect(self.create_vmr).to_be_visible(timeout=10000)
        self.page.wait_for_timeout(2000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Create vmr link is visible",
            attachment_type=allure.attachment_type.PNG
        )

    def create_order_proposal_vmr(self):
        if not self.create_vmr.is_checked():
            self.create_vmr.click()
        expect(self.create_vmr).to_be_checked()
        self.page.wait_for_timeout(2000)

    def select_receiver(self):
        self.receiver.click()
        expect(self.receiver_code.locator("tbody tr").first).to_be_visible(timeout=5000)
        self.receiver_code.locator("tbody tr").first.click()
        expect(self.receiver).not_to_have_value("", timeout=5000)
        self.page.wait_for_timeout(2000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="receiver selection",
            attachment_type=allure.attachment_type.PNG
        )

    def enter_plan_date(self):
        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")
        self.plan_date.fill(today)
        self.page.wait_for_timeout(2000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Plan Date Selection",
            attachment_type=allure.attachment_type.PNG
        )

    def select_article_no(self):
        self.article_no_dropdown.click()
        expect(self.article_no_list.locator("tbody tr").first).to_be_visible(timeout=5000)
        self.article_no_list.locator("tbody tr").first.click()
        expect(self.article_no_list).not_to_be_visible(timeout=5000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Article number selection",
            attachment_type=allure.attachment_type.PNG
        )

    def get_article_numbers_in_grid(self, expected_article_no=None):
        grid = self.page.locator("#grdVmiOrder tbody tr")
        try:
            self.page.wait_for_selector("#grdVmiOrder tbody tr", timeout=5000)
        except Exception:
            print("Grid row did not appear within timeout.")
        rows = grid.all()
        article_numbers = []
        for row in rows:
            try:
                cell = row.locator("td").first
                text = cell.text_content()
                if text:
                    article_numbers.append(text.strip())
            except Exception as e:
                print(f"Error reading row: {e}")
        if expected_article_no:
            assert article_numbers[0] == expected_article_no


    def enter_proposed_qty(self, qty="10"):
        qty_unit_load_val = int(self.qty_unit_load.input_value())
        qty_unit_value = int(qty) // qty_unit_load_val
        self.proposed_qty.press_sequentially(str(qty), delay=100)
        expect(self.proposed_qty).to_have_value(str(qty), timeout=3000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Proposed quantity selection",
            attachment_type=allure.attachment_type.PNG
        )
        return qty_unit_value

    def click_add_article(self):
        article_number_value = self.selected_article_no.input_value()
        self.add_article.click()
        try:
            self.page.wait_for_selector("#grdVmiOrder tbody tr", timeout=8000)
        except Exception:
            print("Grid row did not appear after add article click.")
        return article_number_value

    def create_order_total_pallet_and_verify(self):
        self.total_pallet.click()
        show_order_dropdown = self.page.locator("#mltsel_ddlVmiOrdNo")
        self.page.wait_for_selector("#mltsel_ddlVmiOrdNo", timeout=8000)
        expect(show_order_dropdown).not_to_have_value("", timeout=5000)
        self.page.wait_for_selector("#grdVmiOrder tbody tr", timeout=5000)
        rows = self.page.locator("#grdVmiOrder tbody tr").all()
        assert len(rows) == 1

    def create_order_per_pallet_and_verify(self, qty_unit_value):

        ref = {'value': None}

        def handle_dialog(dialog):
            alert_text = dialog.message
            ref['value'] = alert_text.split(":")[-1].strip()
            allure.attach(
                self.page.screenshot(full_page=True),
                name="Dialog Message",
                attachment_type=allure.attachment_type.PNG
            )
            dialog.accept()

        self.page.on("dialog", handle_dialog)
        self.per_pallet.click()
        show_order_dropdown = self.page.locator('#mltsel_ddlVmiOrdNo')
        self.page.wait_for_selector('#mltsel_ddlVmiOrdNo', timeout=8000)
        expect(show_order_dropdown).to_have_value(ref['value'], timeout=5000)

        grid = self.page.locator("#grdVmiOrder tbody tr")
        try:
            self.page.wait_for_selector("#grdVmiOrder tbody tr", timeout=5000)
        except Exception:
            print("Grid row did not appear within timeout.")
        rows = grid.all()
        # assert len(rows) == qty_unit_value
        allure.attach(
            self.page.screenshot(full_page=True),
            name="vmr creation",
            attachment_type=allure.attachment_type.PNG
        )
        return ref

    def open_vmr_order(self):
        try :
            expect(self.vmr_order_link).to_be_visible(timeout=10000)
            self.vmr_order_link.click()
            self.page.wait_for_load_state("networkidle")
        except  Exception :
            expect(self.create_vmr_proposal_link).to_be_visible(timeout=10000)
            self.create_vmr_proposal_link.click()
            self.page.wait_for_load_state("networkidle")

    def browse_and_upload_file_same_rcv(self):
        assert self.EXCEL_FILE_RCV.exists(), (f"Excel file not found at: {self.EXCEL_FILE_RCV}")
        self.choose_file_button.set_input_files(self.EXCEL_FILE_RCV)
        self.page.wait_for_timeout(2000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="browse_and_upload_file_same_rcv",
            attachment_type=allure.attachment_type.PNG
        )
    def browse_and_upload_diff_file(self):
        assert self.EXCEL_FILE_PATH.exists(), (
            f"Excel file not found at: {self.EXCEL_FILE_PATH}"
        )
        self.choose_file_button.set_input_files(self.EXCEL_FILE_PATH)
        self.page.wait_for_timeout(2000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="browse_and_upload_file_diff_rcv",
            attachment_type=allure.attachment_type.PNG
        )
    def browse_and_upload_file(self):

        # Safety check
        assert self.EXCEL_FILE.exists(), (f"Excel file not found at: {self.EXCEL_FILE}")
        # Upload file using Browse button (same as working code)
        self.choose_file_button.set_input_files(self.EXCEL_FILE)
        # Allow UI to process file selection
        self.page.wait_for_timeout(2000)

    def click_start_upload(self):
        self.start_upload_button.click()
        allure.attach(
            self.page.screenshot(full_page=True),
            name="click_start_upload",
            attachment_type=allure.attachment_type.PNG
        )
        self.page.mouse.click(5, 5)

    def handle_invalid_orders_popup(self):
        try:
            self.popup_close.wait_for(timeout=10000)
            expect(self.export_invalid_orders_button).to_be_visible()
            expect(self.export_invalid_orders_button).to_have_text("Export Invalid orders")
            self.export_invalid_orders_button.click()

            self.popup_close.click()
        except:
            allure.attach(
                "No invalid orders popup appeared",
                "VMR Upload Result",

                allure.attachment_type.TEXT,
            )
        self.page.mouse.click(5, 5)

    def select_upload_vmr_orders(self):
        expect(self.upload_radio).to_be_visible(timeout=10000)
        self.upload_radio.check()
        expect(self.upload_radio).to_be_checked()

    def _init_order_ref_container(self):
        if not hasattr(self, "_order_ref"):
            self._order_ref = {"value": None}

