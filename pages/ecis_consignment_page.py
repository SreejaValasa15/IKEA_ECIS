from playwright.sync_api import Page, expect
import allure
from allure_commons.types import AttachmentType
import os
from pathlib import Path
import re

from pytest_playwright.pytest_playwright import page


class EcisConsignmentPage:
    def __init__(self, page: Page):
        self.page = page

        self.lnk_consignment = page.locator("a:has-text('Consignment')")
        self.btn_create = page.locator("input[value='Create']")
        self.btn_find = page.locator("#btnFind")
        self.popup_consignment_type = page.locator("#divCsmType")
        # self.btn_receiver_dropdown = page.locator("#btnddlRcvCode")
        self.btn_create_new_consignment = page.locator(
            "input[value='Create New Consignment']"
        )
        # self.btn_add_order = page.locator("#btnAddOrder")
        self.btn_find = page.locator("#btnFind")
        # ---------------------
        self.consignments_link = page.locator("a[href = '../Consignment/ConsignmentSummary.aspx']").first
        self.create_consignment_button = page.locator("#btnCreate")
        self.select_receiver_code = page.locator("#btnddlRcvCode")
        self.create_new_consignment_button = page.locator("#btnCreateNew")
        self.dispatch_date = page.locator("#dtpPlanDisp")
        self.lu_type = page.locator("#btnddlLUT")
        self.consignment_grid = page.locator("#grdCsm")
        self.view_btn = page.locator("#btnView")
        self.ship_with_group_btn = page.locator("#btnSWG")
        # ---------------------INVoice-------------------------------------
        self.rdb_dispatch = page.locator("#rdbDispatch")
        self.rdb_invoice = page.locator("#rdbInv")
        self.invoice_button = page.get_by_role("button", name="Invoice")
        self.delete_btn = page.get_by_role("button", name="Delete Consignment")
        self.receiver_dropdown = page.locator("#btnddlRcvCode")
        self.grid_rows = page.locator("#grdCsm tr")
        # ---------------- Export / Import ----------------
        self.btn_export_prodweek = page.locator("#btnExportProdWk")
        self.btn_import_prodweek = page.locator("#btnImportProdWk")

        # Export inside iframe
        self.export_frame = page.frame_locator("iframe")
        self.btn_export_xml = self.export_frame.locator("#btnExportToFile")

        # ---------------- Paths ----------------
        self.PROJECT_ROOT = Path(__file__).resolve().parents[1]

        self.VALID_XML = self.PROJECT_ROOT / "testdata" / "New.xml"
        self.DUPLICATE_XML = self.PROJECT_ROOT / "testdata" / "15653_Prod.xml"



    def screenshot_before(self, page: Page, step_name: str):
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"BEFORE - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass

    def screenshot_after(self, page: Page, step_name: str):
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"AFTER - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass

    def navigate_to_consignment(self):
        self.lnk_consignment.first.click()


    def select_receiver_code_dropdown(self, receiver_code: str):
        self.select_receiver_code.click()
        receiver_cell = self.page.get_by_role("cell", name=receiver_code)
        expect(receiver_cell).to_be_visible(timeout=15000)
        receiver_cell.click()

    def create_new_consignment(self) -> Page:
        self.screenshot_before(self.page, "Click Create New Consignment")

        with self.page.expect_popup() as popup_info:
            self.btn_create_new_consignment.click()

        self.screenshot_after(self.page, "Create New Consignment Clicked")

        popup_page = popup_info.value
        popup_page.wait_for_load_state()

        def accept_dialog(dialog):
            allure.attach(
                dialog.message,
                name="Browser Alert Message",
                attachment_type=allure.attachment_type.TEXT
            )
            dialog.accept()

        popup_page.on("dialog", accept_dialog)

        try:
            # Incoterm dropdown
            incoterm_button = popup_page.locator("#btnddlIncoterm")
            expect(incoterm_button).to_be_visible(timeout=15000)

            incoterm_button.click()
            self.screenshot_after(popup_page, "Incoterm Dropdown Clicked")
            popup_page.evaluate("""
                                () => {
                                    const row = document.querySelector("tr[searchid='DAP']");
                                    if (row) {
                                        row.scrollIntoView({block: 'center'});
                                        row.click();
                                    }
                                }
                                """)
            popup_page.wait_for_timeout(500)
            self.screenshot_after(popup_page, "Incoterm DAP Selected")
            # Add order
            btn_add_order = popup_page.locator("#btnAddOrder")
            expect(btn_add_order).to_be_visible(timeout=30000)

            btn_add_order.click()
            self.screenshot_after(popup_page, "Add Order Clicked")

            expect(
                popup_page.locator("text=Pick Order Lines to Consignment")
            ).to_be_visible(timeout=60000)

        finally:
            popup_page.remove_listener("dialog", accept_dialog)

        return popup_page

    def select_terms_of_delivery(self, popup_page: Page, incoterm_value: str):

        dropdown = popup_page.locator("#btnddlIncotermAddOrder")
        expect(dropdown).to_be_visible(timeout=30000)
        dropdown.click()

        self.screenshot_after(popup_page, "Incoterm Dropdown Clicked - Add Order")
        row = popup_page.locator(
            f"#tblCombo_ddlIncotermAddOrder tr[searchid='{incoterm_value}']"
        ).first

        expect(row).to_be_visible(timeout=15000)
        row.click()

        self.screenshot_after(popup_page, f"Incoterm {incoterm_value} Selected")

    def select_incoterm_add_to_consignment(self, popup_page: Page):

        modal_header = popup_page.locator(
            "text=Pick Order Lines to Consignment"
        )
        expect(modal_header).to_be_visible(timeout=60000)

        # Click Find button
        btn_find = popup_page.locator("#btnFind")

        btn_find.scroll_into_view_if_needed()
        expect(btn_find).to_be_visible(timeout=30000)
        btn_find.click()

        self.screenshot_after(popup_page, "Find Button Clicked")

        order_rows = popup_page.locator("#grdOrderMod tbody tr")
        expect(order_rows.first).to_be_visible(timeout=60000)

        self.screenshot_after(popup_page, "Order Rows Visible")

        # Select all rows
        btn_select_all = popup_page.locator("#grdOrderMod_btnSelectAll")

        btn_select_all.scroll_into_view_if_needed()
        expect(btn_select_all).to_be_visible(timeout=30000)

        self.screenshot_before(popup_page, "Select All Orders")

        btn_select_all.click()

        self.screenshot_after(popup_page, "All Orders Selected")

        # Add lines to consignment
        btn_add_lines = popup_page.locator("#btnAddLines")

        btn_add_lines.scroll_into_view_if_needed()
        expect(btn_add_lines).to_be_visible(timeout=30000)

        def on_dialog(dialog):
            allure.attach(
                dialog.message,
                name="Browser Alert Message",
                attachment_type=allure.attachment_type.TEXT
            )
            dialog.accept()

        popup_page.once("dialog", on_dialog)
        with popup_page.expect_event("dialog"):
            btn_add_lines.click()

        popup_page.wait_for_load_state("domcontentloaded")
        self.screenshot_after(popup_page, "After Add Lines to Consignment (Alert Accepted)")
        popup_page.close()
        self.page.wait_for_timeout(2000)

    def click_consignments_link(self):
        # expect(self.consignments_link).to_be_visible(timeout=10000)
        self.consignments_link.click()
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.screenshot_after(self.page, "Click Consignments Link")

    def create_consignment(self):
        self.create_consignment_button.click()
        self.page.wait_for_timeout(4000)
        self.screenshot_after(self.page, "Add Consignments")

    def select_receiver(self, receiver_code):
        self.select_receiver_code.click()
        receiver_grid = self.page.locator("#tblCombo_ddlRcvCode tbody tr")
        row_count = receiver_grid.count()
        for i in range(row_count):
            row = receiver_grid.nth(i)
            receiver_text = row.locator("td").nth(0).inner_text().split("-")[0].strip()
            if receiver_text == receiver_code:
                row.click()
                break
        self.page.wait_for_timeout(2000)
        self.screenshot_after(self.page, "Receiver Selection")

    def click_create_new_consignment(self):
        with self.page.expect_popup() as popup_info:
            self.create_new_consignment_button.click()
        popup = popup_info.value

        allure.attach(
            popup.screenshot(full_page=True),
            name="Create New Consignment - Opened",
            attachment_type=AttachmentType.PNG
        )
        popup.evaluate("document.body.style.zoom = '70%'")
        # Click Add Order
        popup.locator("#btnAddOrder").click()
        popup.wait_for_timeout(2000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="After Clicking Add Order",
            attachment_type=AttachmentType.PNG
        )

        row = popup.locator("#grdOrderMod tbody tr").first
        row.locator("td").first.locator("input").check()
        popup.wait_for_timeout(2000)


        allure.attach(
            popup.screenshot(full_page=True),
            name="Order Selected",
            attachment_type=AttachmentType.PNG
        )


        popup.locator("#btnAddLines").click()
        popup.wait_for_timeout(2000)

        # Screenshot 4 – lines added
        allure.attach(
            popup.screenshot(full_page=True),
            name="Order Lines Added to Consignment",
            attachment_type=AttachmentType.PNG
        )
        order_id = popup.locator("input[name='txtCsmNo']").input_value()
        popup.close()
        self.page.wait_for_timeout(2000)
        return order_id


    def verify_consignment_in_grid(self, consign_id):
        screenshot_bytes = self.page.screenshot(full_page=True)
        self.page.wait_for_timeout(2000)
        self.page.locator("#btnClear").click()
        self.page.wait_for_timeout(2000)
        self.page.locator("#btnddlCsm").click(force=True)
        self.page.locator("#mltsel_ddlCsm").click()
        self.page.locator("#mltsel_ddlCsm").press_sequentially(consign_id, delay=100)
        self.page.locator("#btnFind").click()
        self.page.wait_for_timeout(2000)
        allure.attach(
            screenshot_bytes,
            name="Consignment creation verification in grid",
            attachment_type=AttachmentType.PNG
        )

    def select_consignment_to_dispatch(self, cons_code):
        screenshot_bytes = self.page.screenshot(full_page=True)
        consignment_row = self.consignment_grid.locator("tbody tr")
        row_count = consignment_row.count()
        for i in range(row_count):
            row = consignment_row.nth(i)
            cons_text = row.locator("td").nth(1).inner_text().strip()
            imported_text = row.locator("td").nth(10).inner_text().strip()
            status_text = row.locator("td").nth(4).inner_text().strip()
            if cons_code == cons_text and status_text == "Trp Booked":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break

            self.page.wait_for_timeout(1000)
            allure.attach(
                screenshot_bytes,
                name="Consignment Selection - Dispatch",
                attachment_type=AttachmentType.PNG
            )

    def select_consignment_to_book_trip(self, cons_code):
        self.screenshot_before(self.page, "Selecting Consignment")
        consignment_row = self.consignment_grid.locator("tbody tr")
        expect(consignment_row.first).to_be_visible(timeout=10000)
        row_count = consignment_row.count()

        for i in range(row_count):
            row = consignment_row.nth(i)

            cons_text = row.locator("td").nth(1).inner_text().strip()
            status_text = row.locator("td").nth(4).inner_text().strip()
            imported_text = row.locator("td").nth(10).inner_text().strip()
            if cons_code == cons_text and status_text == "Created":
            # if rce_code in rce_text and imported_text == "Missing" and status_text == "Created":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                self.screenshot_after(self.page, "Consignment Selected")
                break

    def select_consignment_to_modify_book_trip(self, rce_code):
        screenshot_bytes = self.page.screenshot(full_page=True)

        consignment_row = self.consignment_grid.locator("tbody tr")
        row_count = consignment_row.count()
        global consign_id
        for i in range(row_count):
            row = consignment_row.nth(i)
            consign_id = row.locator("td").nth(1).inner_text().strip()
            rce_text = row.locator("td").nth(2).inner_text().strip()
            status_text = row.locator("td").nth(4).inner_text().strip()
            ship_with_group_text = row.locator("td").nth(8).inner_text().strip()
            imported_text = row.locator("td").nth(10).inner_text().strip()

            if (
                    rce_code in rce_text
                    and status_text == "Created"
                    and imported_text == "Missing"
                    and ship_with_group_text != ""
            ):
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()
                break

        self.page.wait_for_timeout(1000)

        allure.attach(
            screenshot_bytes,
            name="Consignment Selection - Modify Book Trip",
            attachment_type=AttachmentType.PNG
        )

        self.page.wait_for_timeout(2000)

        with self.page.expect_popup() as popup_info:
            self.ship_with_group_btn.click()
            self.page.wait_for_timeout(2000)

        popup = popup_info.value

        allure.attach(
            popup.screenshot(full_page=True),
            name="ShipWithGroupSummary Popup Opened",
            attachment_type=AttachmentType.PNG
        )

        popup.wait_for_timeout(2000)

        shipgrouprow = popup.locator("#grdSWG tbody tr")
        ship_row_count = shipgrouprow.count()

        for i in range(ship_row_count):
            row = shipgrouprow.nth(i)
            consignment_no = row.locator("td").nth(2).inner_text().strip()

            if consignment_no == consign_id:
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()
                break

        allure.attach(
            popup.screenshot(full_page=True),
            name="ShipWithGroup Consignment Selected",
            attachment_type=AttachmentType.PNG
        )

        popup.wait_for_timeout(2000)

        with popup.expect_popup() as new_popup_info:
            popup.locator("#btnModifySWG").click()

        new_popup = new_popup_info.value
        screenshot_byte = new_popup.screenshot(full_page=True)

        new_popup.wait_for_timeout(2000)

        # expect(new_popup).to_have_url(
        #     "https://ecis-ofp.apps.ikeadt.com/Consignment/ConsignmentLines.aspx"
        # )

        new_popup.evaluate("document.body.style.zoom = '70%'")
        new_popup.wait_for_timeout(2000)
        allure.attach(
            new_popup.screenshot(full_page=True),
            name="Consignment ModifyShipWithGroup - Before",
            attachment_type=AttachmentType.PNG
        )
        new_popup.locator("#btnddlSWG").click()
        new_popup.wait_for_timeout(1000)
        new_popup.locator("#tblCombo_ddlSWG tbody tr").nth(1).click()
        new_popup.locator("#btnAdd").click()
        allure.attach(
            new_popup.screenshot(full_page=True),
            name="Consignment ModifyShipWithGroup - After",
            attachment_type=AttachmentType.PNG
        )
        new_popup.close()
        popup.close()

    def view_consignment_details_book_trip(self):
        self.page.wait_for_timeout(2000)

        with self.page.expect_popup() as popup_info:
            self.view_btn.click()
        popup = popup_info.value

        # expect(popup).to_have_url(
        #     "https://ecis-ofp.apps.ikeadt.com/Consignment/Consignment.aspx"
        # )
        popup.wait_for_load_state("networkidle")

        allure.attach(
            popup.screenshot(full_page=True),
            name="Book Trip - Popup Opened",
            attachment_type=allure.attachment_type.PNG
        )

        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")
        popup.evaluate("document.body.style.zoom = '70%'")
        popup.wait_for_timeout(2000)
        date_field = popup.locator("#dtpPlanDisp")
        date_field.click()
        date_field.press("Control+A")
        date_field.press("Backspace")
        date_field.fill(today)
        date_field.click()

        popup.wait_for_timeout(1000)

        popup.locator("#btnddlLUT").click()
        popup.wait_for_timeout(1000)

        popup.locator("#tblCombo_ddlLUT tbody tr").nth(1).click()
        popup.wait_for_timeout(2000)

        def handle_dialog(dialog):
            print(dialog.message)
            assert "Do you really want to book" in dialog.message
            dialog.accept()

        popup.on("dialog", handle_dialog)
        popup.locator("#btnBookTrp").click()
        popup.close()


    def view_consignment_details_dispatch(self):
        self.page.wait_for_timeout(2000)

        with self.page.expect_popup() as popup_info:
            self.view_btn.click()
            self.page.wait_for_timeout(2000)
        popup = popup_info.value

        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")
        popup.wait_for_timeout(2000)
        popup.evaluate("document.body.style.zoom = '70%'")
        popup.wait_for_timeout(2000)
        popup.locator("#grdCsmLines_btnSelectAll").click()
        popup.locator("#dtpCarArrDate").fill(today)
        popup.locator("#ddlCarArrTimeHrMin_spinUpButton").click(click_count=2)
        popup.wait_for_timeout(4000)
        allure.attach(
            popup.screenshot(full_page=True),
            name="Dispatch - Consignment Popup Opened",
            attachment_type=AttachmentType.PNG
        )
        with popup.expect_popup() as new_popup_info:
            popup.locator("#btnChange").click()
        new_popup = new_popup_info.value
        screenshot_byte = new_popup.screenshot(full_page=True)
        new_popup.wait_for_timeout(2000)
        # expect(new_popup).to_have_url(
        #     "https://ecis-ofp.apps.ikeadt.com/Consignment/ConsignmentLines.aspx"
        # )
        new_popup.locator("#grdCsmLines_btnSelectAll").click()
        new_popup.wait_for_timeout(2000)
        new_popup.locator("#dtpProdWeek").fill(today)
        new_popup.wait_for_timeout(2000)
        new_popup.locator("#btnProdWeek").click()
        new_popup.wait_for_timeout(2000)
        allure.attach(
            new_popup.screenshot(full_page=True),
            name="Dispatch - Production Week Set",
            attachment_type=AttachmentType.PNG
        )
        new_popup.wait_for_timeout(2000)
        new_popup.close()

        def handle_dialog(dialog):
            assert "Do you really want to dispatch consignment" in dialog.message
            dialog.accept()

        popup.wait_for_timeout(2000)
        popup.locator("#dtpDispDate").fill(today)
        popup.locator("#ddlDispTimeHrMin_spinUpButton").click(click_count=3)
        popup.locator("#txtSealNo1").click()
        popup.on("dialog", handle_dialog)
        popup.locator("#btnDispatch").click()

        popup.close()

    def select_planned_dispatch_date(self):
        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")

        self.screenshot_before("Planned Dispatch Date Selection")
        self.dispatch_date.fill(today)
        self.page.wait_for_timeout(2000)
        self.screenshot_after("Planned Dispatch Date Selected")

    def select_lu_type(self):
        self.screenshot_before("LU Type Selection")
        self.lu_type.click()
        select_all_btn = self.page.locator("#tblCombo_ddlLUT tbody tr").nth(1)
        select_all_btn.click()
        self.page.wait_for_timeout(2000)
        self.screenshot_after("LU Type Selected")

    def select_consignment_to_ship_with_group(self, rce_code):
        screenshot_bytes = self.page.screenshot(full_page=True)
        consignment_row = self.consignment_grid.locator("tbody tr")
        row_count = consignment_row.count()
        for i in range(row_count):
            row = consignment_row.nth(i)
            global consignment_id
            consignment_id = row.locator("td").nth(1).inner_text().strip()
            rce_text = row.locator("td").nth(2).inner_text().strip()
            status_text = row.locator("td").nth(4).inner_text().strip()
            ship_with_group_text = row.locator("td").nth(8).inner_text().strip()
            imported_text = row.locator("td").nth(10).inner_text().strip()
            if rce_code in rce_text and status_text == "Created" and imported_text == "Missing" and ship_with_group_text == "":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break

        self.page.wait_for_timeout(1000)
        allure.attach(
            screenshot_bytes,
            name="Consignment Selection - ShipWithGroup Selected",
            attachment_type=AttachmentType.PNG
        )
        self.page.wait_for_timeout(2000)

        with self.page.expect_popup() as popup_info:
            self.ship_with_group_btn.click()
            self.page.wait_for_timeout(2000)
        popup = popup_info.value
        allure.attach(
            popup.screenshot(full_page=True),
            name=" ShipWithGroupSummary Popup Opened",
            attachment_type=AttachmentType.PNG
        )
        popup.wait_for_timeout(2000)
        shipgrouprow = popup.locator("#grdSWG tbody tr")
        ship_row_count = shipgrouprow.count()
        for i in range(ship_row_count):
            row = shipgrouprow.nth(i)
            consignment_no = row.locator("td").nth(2).inner_text().strip()
            if consignment_no == consignment_id:
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break

        allure.attach(
            popup.screenshot(full_page=True),
            name=" ShipWithGroup Consignment Selected",
            attachment_type=AttachmentType.PNG
        )
        popup.wait_for_timeout(2000)
        popup.locator("#btnGenerateSWG").click()

        allure.attach(
            popup.screenshot(full_page=True),
            name=" ShipWithGroup ID Generated",
            attachment_type=AttachmentType.PNG
        )

        popup.wait_for_timeout(2000)
        popup.close()
        allure.attach(
            screenshot_bytes,
            name="Consignment Selection - ShipWithGroup Id Generated",
            attachment_type=AttachmentType.PNG
        )

    def click_create_new_consignment_withshipgroup(self):
        with self.page.expect_popup() as popup_info:
            self.create_new_consignment_button.click()
        popup = popup_info.value


        allure.attach(
            popup.screenshot(full_page=True),
            name="Create New Consignment - Opened",
            attachment_type=AttachmentType.PNG
        )
        popup.evaluate("document.body.style.zoom = '70%'")
        # Click Add Order
        popup.locator("#btnAddOrder").click()
        popup.wait_for_timeout(2000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="After Clicking Add Order",
            attachment_type=AttachmentType.PNG
        )

        row = popup.locator("#grdOrderMod tbody tr").first
        row.locator("td").first.locator("input").check()
        popup.wait_for_timeout(2000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="Order Selected",
            attachment_type=AttachmentType.PNG
        )

        popup.locator("#btnAddLines").click()
        popup.wait_for_timeout(2000)

        # Screenshot 4 – lines added
        allure.attach(
            popup.screenshot(full_page=True),
            name="Order Lines Added to Consignment",
            attachment_type=AttachmentType.PNG
        )
        popup.locator("#chkCPTrp").click()
        allure.attach(
            popup.screenshot(full_page=True),
            name="CP Delivery Check box selected",
            attachment_type=AttachmentType.PNG
        )
        popup.wait_for_timeout(2000)

        def handle_save_dialog(dialog):
            assert "Data Saved Successfully" in dialog.message
            dialog.accept()

        popup.on("dialog", handle_save_dialog)
        popup.locator("#btnSave").click()

        popup.close()
        self.page.wait_for_timeout(2000)
        allure.attach(
            self.page.screenshot(full_page=True),
            name="Consignment Created",
            attachment_type=AttachmentType.PNG
        )
        self.page.wait_for_timeout(2000)

    # =========================================================

    def get_valid_sscc(self):
        return str(self.VALID_XML)

    def validate_file_exists(self, file_path: str):
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def export_prodweek_sscc(self):
        self.screenshot_before(self.page, "Click Export")
        self.btn_export_prodweek.click()

        with self.page.expect_download() as download_info:
            self.btn_export_xml.click()

        download = download_info.value
        self.screenshot_after(self.page, "XML Exported")
        return download

    def open_import_popup(self) -> Page:
        self.screenshot_before(self.page, "Open Import Popup")

        with self.page.expect_popup() as popup_info:
            self.btn_import_prodweek.click()

        popup_page = popup_info.value
        popup_page.wait_for_load_state()

        self.screenshot_after(popup_page, "Import Popup Opened")
        return popup_page

    def click_export_to_xml(self):

        self.screenshot_before(self.page, "Click Export To XML")

        self.page.locator("#btnExportProdWk").click()

        with self.page.expect_download() as download_info:
            self.page.frame_locator("iframe").locator("#btnExportToFile").click()

        download = download_info.value
        self.screenshot_after(self.page, "XML Downloaded")
        self._close_export_popup()
        return download

    def _close_export_popup(self):

        close_btn = self.page.locator("#cboxClose")
        close_btn.wait_for(state="visible", timeout=5000)
        close_btn.click()
        self.screenshot_after(self.page, "Export Popup Closed")

    def select_created_consignment(self):

        self.screenshot_before(self.page, "Select Created Consignment")
        rows = self.consignment_grid.locator("tbody tr")
        expect(rows.first).to_be_visible(timeout=10000)
        row_count = rows.count()

        for i in range(row_count):
            row = rows.nth(i)
            status_text = row.locator("td").nth(4).text_content().strip()

            if status_text.lower() == "created":
                checkbox = row.locator("td").first.locator("input[type='checkbox']")
                checkbox.check()

                self.screenshot_after(self.page, "Created Consignment Selected")
                return
        raise Exception("No consignment found with status 'Created'")


    def browse_and_upload_valid_sscc(self, popup_page: Page):

        file_path = Path(self.get_valid_sscc())
        assert file_path.exists(), f"File not found at: {file_path}"
        self.screenshot_before(popup_page, "Upload Valid SSCC File")
        file_inputs = popup_page.locator("input[type='file']")
        file_input = None
        for i in range(file_inputs.count()):
            el = file_inputs.nth(i)
            if el.is_visible():
                file_input = el
                break

        if file_input is None:
            raise Exception("No visible file input found")
        file_input.set_input_files(file_path)
        popup_page.wait_for_timeout(2000)
        self.screenshot_after(popup_page, "File Selected")
        start_btn = popup_page.locator("#startImport")

        if start_btn.is_enabled():
            start_btn.click()
            dialog = popup_page.wait_for_event("dialog", timeout=15000)
            allure.attach(dialog.message, "Dialog Message", AttachmentType.TEXT)
            assert "Consignment lines updated" in dialog.message
            dialog.accept()
        else:
            raise Exception("Start Import still disabled")

        popup_page.close()

    def click_view_consignment(self):

        self.screenshot_before(self.page, "Click View")
        with self.page.expect_popup() as popup_info:
            self.view_btn.click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        popup.wait_for_url("**Consignment.aspx", timeout=20000)

        popup.evaluate("document.body.style.zoom = '70%'")
        self.screenshot_after(popup, "View Popup Opened")
        return popup

    def capture_order_and_click_change(self, popup):

        popup.wait_for_timeout(2000)
        popup.evaluate("document.body.style.zoom = '70%'")
        popup.wait_for_timeout(2000)

        try:
            row = popup.locator("#grdCsm tbody tr").first
            if row.is_visible():
                order_number = row.locator("td").nth(1).text_content().strip()
            else:
                order_number = None
        except:
            order_number = None

        popup.locator("#grdCsmLines_btnSelectAll").click()
        popup.wait_for_timeout(1000)

        with popup.expect_popup() as new_popup_info:
            popup.locator("#btnChange").click()
        popup.wait_for_timeout(2000)
        popup.close()
        new_popup = new_popup_info.value
        new_popup.wait_for_timeout(2000)
        new_popup.locator("#grdCsmLines_btnSelectAll").click()
        new_popup.wait_for_timeout(2000)
        return order_number, new_popup

    def open_dwp_popup(self, new_popup):

        self.screenshot_before(new_popup, "Open DWP Popup")
        new_popup.wait_for_timeout(2000)
        dwp_btn = new_popup.locator("text=Show/Change DWP")
        dwp_btn.scroll_into_view_if_needed()
        new_popup.wait_for_timeout(500)
        dwp_btn.click()
        new_popup.locator("#mltsel_ddlDwpArtNo").wait_for(timeout=15000)
        self.screenshot_after(new_popup, "DWP Popup Opened")

    def validate_order_in_dwp(self, new_popup, expected_order):
        new_popup.wait_for_timeout(2000)
        new_popup.locator("#mltsel_ddlDwpArtNo").wait_for(timeout=15000)
        self.screenshot_after(new_popup, "Order Validation Completed")
        new_popup.wait_for_timeout(2000)
        new_popup.close()

    def select_dispatch_and_check(self, dispatch_id: str):
        self.rdb_dispatch.check()
        self.screenshot_after(self.page, "Dispatched/invoice radio button is checked")

        row = self.page.get_by_role("row", name=re.compile(dispatch_id))

        row.locator("td[aria-describedby='grdCsm_CsmNo']").click()

        row.locator("#grdCsm_selectedRows").check()

        self.screenshot_after(self.page, "Order is selected for invoice")

    def open_invoice_popup(self) -> Page:
        with self.page.expect_popup() as popup_info:
            self.invoice_button.click()

        popup_page = popup_info.value
        popup_page.wait_for_load_state()

        allure.attach(
            popup_page.screenshot(),
            name="Invoice Popup Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        return popup_page

    def create_invoice(self, popup_page: Page, dispatch_id: str):

        popup_page.locator("#txtInvoiceId").fill(f"{dispatch_id}INV")

        allure.attach(
            popup_page.screenshot(),
            name="After filling Invoice ID",
            attachment_type=allure.attachment_type.PNG
        )
        from datetime import datetime
        today = str(datetime.today().day)

        popup_page.get_by_title("Show calendar").click()
        popup_page.get_by_role("link", name=today, exact=True).click()

        allure.attach(
            popup_page.screenshot(),
            name="After selecting invoice date",
            attachment_type=allure.attachment_type.PNG
        )

        popup_page.once("dialog", lambda d: d.accept())
        popup_page.get_by_role("button", name="Send Invoice").click()

        allure.attach(
            popup_page.screenshot(),
            name="After clicking Send Invoice",
            attachment_type=allure.attachment_type.PNG
        )

    def validate_invoice_dispatch(self, dispatch_id: str):
        self.rdb_invoice.check()
        self.screenshot_after(self.page, "Invoice Radio button is checked")

        cell = self.page.get_by_role(
            "gridcell", name=dispatch_id, exact=True
        )

        # expect(cell).to_be_visible(timeout=10000)
        cell.click()
        self.screenshot_after(self.page, "Validating the order is invoiced")

    def new_create_consignment(self, receiver_code: str) -> str:
        self.btn_create.click()
        self.screenshot_after(self.page, "Click on Create")
        self.receiver_dropdown.click()
        self.screenshot_after(self.page, "Dropdown")
        self.page.get_by_role("cell", name=receiver_code).click()
        self.screenshot_after(self.page, "Selecting reciever Code")
        with self.page.expect_popup() as popup_info:
            self.btn_create_new_consignment.click()

        popup = popup_info.value
        popup.wait_for_load_state()
        popup.wait_for_timeout(5000)
        order_id = popup.locator("input[name='txtCsmNo']").input_value()

        print(f" Created CSM No: {order_id}")

        popup.close()

        if not order_id:
            raise Exception(" Failed to capture CSM No")

        return order_id

    def do_select_created_consignment(self, order_id: str):
        print(f" Waiting for row: {order_id}")

        row = self.page.locator("#grdCsm tr").filter(has_text=order_id)
        row.first.wait_for()

        print(f" Row found: {order_id}")

        checkbox = row.locator("input[type='checkbox']").first
        checkbox.click()
        self.screenshot_after(self.page, "Selecting Consignment")

    def delete_consignment(self, order_id: str):
        dialog_messages = []

        def handle_dialog(dialog):
            msg = dialog.message
            print(f"Dialog: {msg}")
            dialog_messages.append(msg)
            self.page.wait_for_timeout(3000)
            dialog.accept()
            self.page.wait_for_timeout(3000)

        self.page.on("dialog", handle_dialog)

        self.delete_btn.click()
        self.screenshot_after(self.page, "Delete Consignment")

        self.page.wait_for_timeout(3000)