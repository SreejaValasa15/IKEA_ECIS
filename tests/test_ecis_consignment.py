
import allure
import pytest
from testdata.ecis_consignment_data import TEST_CREATE_CONSIGNMENT_DISPATCH
from testdata.ecis_consignment_data import TEST_SHIP_WITH_GRPOUP
from testdata.ecis_consignment_data import TEST_DISPATCH_TO_INVOICE
from testdata.ecis_consignment_data import TEST_CREATE_AND_DELETE_CONSIGNMENT
from testdata.ecis_consignment_data import TEST_UPLOAD_VALID_SSCC
from testdata.ecis_consignment_data import TEST_SHOW_DWP_DATA
from testdata.ecis_consignment_data import TEST_SELECT_DIFF_INCOTERM_CONSIGNMENT
from testdata.ecis_consignment_data import TEST_ECIS_CREATE_CONSIGNMENT
from testdata.ecis_consignment_data import TEST_ECIS_BOOK_TRIP_CONSIGNMENT
from testdata.ecis_consignment_data import TEST_ECIS_DISPATCH_CONSIGNMENT
from testdata.ecis_consignment_data import TEST_ECIS_SHIPWITHGROUP_CONSIGNMENT
from testdata.ecis_consignment_data import TEST_ECIS_SWG_GRID_REFRESH

@allure.feature("Consignment")
@allure.story("Validate successful SSCC upload")
@pytest.mark.parametrize("test_data", TEST_UPLOAD_VALID_SSCC)
def test_upload_valid_sscc(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        oder_maintenance_page,
        ecis_consignment_page,
        *_
    ) = ecis_dashboard_page

    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Navigate to Dashboard"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("Open Consignment Page"):
        ecis_consignment_page.navigate_to_consignment()

    with allure.step("Select consignment"):
        ecis_consignment_page.select_created_consignment()


    with allure.step("Export ProdWeek/SSCC"):
        ecis_consignment_page.click_export_to_xml()


    with allure.step("Open Import Popup"):
        popup_page = ecis_consignment_page.open_import_popup()

    with allure.step("Upload valid XML file"):
        ecis_consignment_page.browse_and_upload_valid_sscc(popup_page)

@allure.story("Validate DWP values for selected order line")
@pytest.mark.parametrize("test_data", TEST_SHOW_DWP_DATA)
def test_show_dwp_data(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,
    ) = ecis_dashboard_page

    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Navigate to Consignment"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("Select Created Consignment"):
        ecis_consignment_page.navigate_to_consignment()
        ecis_consignment_page.select_created_consignment()

    with allure.step("Click View"):
        popup_page = ecis_consignment_page.click_view_consignment()

    with allure.step("Capture Order and Open Context Menu"):
        order_no,new_popup  = ecis_consignment_page.capture_order_and_click_change(popup_page)

    with allure.step("Open DWP Popup"):
        ecis_consignment_page.open_dwp_popup(new_popup)

    with allure.step("Validate Order in DWP"):
        ecis_consignment_page.validate_order_in_dwp(new_popup, order_no)


@allure.story("Validate Terms mismatch when selecting different Incoterm")
@pytest.mark.parametrize("data", TEST_SELECT_DIFF_INCOTERM_CONSIGNMENT)
def test_select_diff_incoterm_consignment(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,
    ) = ecis_dashboard_page


    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("Click on Consignment menu"):
        ecis_consignment_page.navigate_to_consignment()

    with allure.step("Click on create consignment button"):
        ecis_consignment_page.create_consignment()

    with allure.step("Select Receiver"):
        ecis_consignment_page.select_receiver_code_dropdown(data["rvc_code"])

    with allure.step("Click create new consignment button"):
        popup_page = ecis_consignment_page.create_new_consignment()

    with allure.step("Select FCA as Terms of Delivery in Pick Order Lines"):
        ecis_consignment_page.select_terms_of_delivery(
            popup_page=popup_page,
            incoterm_value=data["incoterm"]
        )

    with allure.step("Click Find and Select All order lines"):
        ecis_consignment_page.select_incoterm_add_to_consignment(popup_page)


@allure.story("Creation of Consignment from Created to Dispatch")
@pytest.mark.parametrize("data", TEST_ECIS_CREATE_CONSIGNMENT)
def test_ecis_create_consignment(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,
    ) = ecis_dashboard_page

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("click on create button"):
        ecis_consignment_page.create_consignment()

    with allure.step("Select Receiver"):
        ecis_consignment_page.select_receiver(data["rvc_code"])

    with allure.step("click create new consignment button"):
        ecis_consignment_page.click_create_new_consignment()

@allure.story("Creation of Consignment from Created to Tripbook")
@pytest.mark.parametrize("data", TEST_ECIS_BOOK_TRIP_CONSIGNMENT)
def test_ecis_book_trip_consignment(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,
    ) = ecis_dashboard_page


    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("select the consignment to book trip"):
        ecis_consignment_page.select_consignment_to_book_trip(data["rvc_code"])

    with allure.step("click on view consignment details and Book Trip"):
        ecis_consignment_page.view_consignment_details_book_trip()

@allure.story("Creation of Consignment from Created to Dispatch")
@pytest.mark.parametrize("data", TEST_ECIS_DISPATCH_CONSIGNMENT)
def test_ecis_dispatch_consignment(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,

    ) = ecis_dashboard_page

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("select the consignment to book trip"):
        ecis_consignment_page.select_consignment_to_book_trip(data["rvc_code"])

    with allure.step("click on view consignment details and Book Trip"):
        ecis_consignment_page.view_consignment_details_book_trip()
    with allure.step("select the consignment to dispatch"):
        ecis_consignment_page.select_consignment_to_dispatch(data["rvc_code"])

    with allure.step("click on view consignment details and dispatch"):
        ecis_consignment_page.view_consignment_details_dispatch()

@allure.story("Creation of Consignment  with  ShipWithGroup ")
@pytest.mark.parametrize("data",TEST_ECIS_SHIPWITHGROUP_CONSIGNMENT)
def test_ecis_shipwithgroup_consignment(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,

    ) = ecis_dashboard_page

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("click on create button"):
        ecis_consignment_page.create_consignment()

    with allure.step("Select Receiver"):
        ecis_consignment_page.select_receiver(data["rvc_code"])

    with allure.step("click create new consignment with ship group"):
        ecis_consignment_page.click_create_new_consignment_withshipgroup()

    with allure.step("Select the consignment for ship with group"):
        ecis_consignment_page.select_consignment_to_ship_with_group(data["rvc_code"])

@allure.story("Verify that the data in the SWG grid is refreshed after the modification of consignment")
@pytest.mark.parametrize("data", TEST_ECIS_SWG_GRID_REFRESH)
def test_ecis_swg_grid_refresh(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,

    ) = ecis_dashboard_page

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("click on create button"):
        ecis_consignment_page.create_consignment()

    with allure.step("Select Receiver"):
        ecis_consignment_page.select_receiver(data["rvc_code"])

    with allure.step("click create new consignment with ship group"):
        ecis_consignment_page.click_create_new_consignment_withshipgroup()

    with allure.step("Select the consignment to book trip"):
        ecis_consignment_page.select_consignment_to_modify_book_trip(data["rvc_code"])

@allure.story("Invoice the Consignment")
@pytest.mark.parametrize("test_data", TEST_DISPATCH_TO_INVOICE)
def test_dispatch_to_invoice(ecis_dashboard_page, test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,

    ) = ecis_dashboard_page
    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("Select dispatch using test data"):
        ecis_consignment_page.select_dispatch_and_check(test_data["dispatch_id"])

    with allure.step("Open invoice popup"):
        popup_page = ecis_consignment_page.open_invoice_popup()

    with allure.step("Create invoice with today's date"):
        ecis_consignment_page.create_invoice(popup_page, test_data["dispatch_id"])
        popup_page.close()

    with allure.step("Validate same dispatch ID in Invoice tab"):
        ecis_consignment_page.validate_invoice_dispatch(test_data["dispatch_id"])


@allure.story("Delete functionality")
@pytest.mark.parametrize("data", TEST_CREATE_AND_DELETE_CONSIGNMENT)
def test_create_and_delete_consignment(ecis_dashboard_page,data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        ecis_consignment_page,
        *_,

    ) = ecis_dashboard_page

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()
    with allure.step("Navigating to consignment page"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()
        ecis_consignment_page.click_consignments_link()

    with allure.step("Create Consignment"):
        order_id = ecis_consignment_page.new_create_consignment(data["rvc_code"])
    with allure.step("Select created consignment"):
        ecis_consignment_page.do_select_created_consignment(order_id)
    with allure.step("Delete Consignment"):
        ecis_consignment_page.delete_consignment(order_id)
