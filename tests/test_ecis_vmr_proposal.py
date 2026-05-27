import allure
import pytest

from testdata.ecis_vmr_proposal_data import (TEST_DATA_CREATE_ORDER_PER_PALLET)
from testdata.ecis_vmr_proposal_data import (TEST_ECIS_CREATE_ORDER_TOTAL_PALLET)
from testdata.ecis_vmr_proposal_data import (TEST_ECIS_VMR_PROPOSAL_SEARCH)
from testdata.ecis_vmr_proposal_data import (TEST_ECIS_VIEW_VMR_PROPOSAL_COLUMNS)
from testdata.ecis_vmr_proposal_data import (TEST_VMR_VIEW_FLOW)
from testdata.ecis_vmr_proposal_data import (TEST_FIND_AND_CLEAR)
from testdata.ecis_vmr_proposal_data import (TEST_ECIS_VMR_UPLOAD)
from testdata.ecis_vmr_proposal_data import (TEST_VERIFY_EXPORT_FILE)
from testdata.ecis_vmr_proposal_data import (TEST_ECIS_CREATE_VMR_DIFFERENT_RCV_ARTICLE_BULK_UPLOAD)
from testdata.ecis_vmr_proposal_data import (TEST_VERIFY_ORDER_STATUS_SENT_PROPOSAL)
from testdata.ecis_vmr_proposal_data import (TEST_VERIFY_RCV_COLUMNS)
@allure.feature("VMR Proposal")
@allure.story("Verify that creating VMR proposals on the same day is possible for the same supplier with the same RCV & Article combination using 'Create per Pallet' option")
@pytest.mark.parametrize('data', TEST_DATA_CREATE_ORDER_PER_PALLET)
def test_ecis_create_order_per_pallet(ecis_dashboard_page,data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page

    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Open File Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()

    with allure.step("Create VMR Proposal"):
        create_vmr_page.create_vmr_proposal()
        create_vmr_page.create_order_proposal_vmr()
        create_vmr_page.select_receiver()
        create_vmr_page.enter_plan_date()
        create_vmr_page.select_article_no()
        qty_unit_value = create_vmr_page.enter_proposed_qty(qty=data["quantity"])
        article_number_value = create_vmr_page.click_add_article()

    with allure.step("Validate Article in Grid"):
        create_vmr_page.get_article_numbers_in_grid(expected_article_no=article_number_value)

    with allure.step("Create Order Per Pallet and Verify"):
        create_vmr_page.create_order_per_pallet_and_verify(data["quantity"])

@allure.story("Verify that creating VMR proposals on the same day is possible for the same supplier with the same RCV & Article combination using 'Create Order Total Pallet' option")
@allure.story("Verify that the entered quantity is split correctly according to DWP rules")
@pytest.mark.parametrize("data", TEST_ECIS_CREATE_ORDER_TOTAL_PALLET)
def test_ecis_create_order_total_pallet(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Open File Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()

    with allure.step("Create VMR Proposal"):
        create_vmr_page.create_vmr_proposal()
        create_vmr_page.create_order_proposal_vmr()
        create_vmr_page.select_receiver()
        create_vmr_page.enter_plan_date()
        create_vmr_page.select_article_no()
        create_vmr_page.enter_proposed_qty(qty=data["quantity"])
        article_number_value = create_vmr_page.click_add_article()

    with allure.step("Validate Article in Grid"):
        create_vmr_page.get_article_numbers_in_grid(expected_article_no=article_number_value)

    with allure.step("Create Order Total Pallet and Verify"):
        create_vmr_page.create_order_total_pallet_and_verify()

@allure.story("Verify that the Search filter is available in the top of the screen")
@allure.story("Verify that all the search options are available")
@pytest.mark.parametrize("data", TEST_ECIS_VMR_PROPOSAL_SEARCH)
def test_ecis_view_vmr_proposal_search_filter(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Open File Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()

    with allure.step("Click on 'View VMR Proposal'"):
        dashboard_page.select_view_vmr_proposal()

    with allure.step("Verify that the system displays the search filters in the top of the screen."):
        view_vmr_page.verify_search_filters_visible()

    with allure.step("Verify that all the search options are available"):
        view_vmr_page.verify_search_options_available()

    with allure.step("Click on VMR Ord Ref filter drop down and verify list and input"):
        view_vmr_page.open_and_verify_vmr_order_ref_dropdown()

    with allure.step("Click on RCV_Code filter drop down and verify list and input"):
        view_vmr_page.open_and_verify_rcv_code_dropdown()

    with allure.step("Click on END_RCV filter drop down and verify list and input"):
        view_vmr_page.open_and_verify_end_rcv_dropdown()

    with allure.step("Click on Art No filter drop down and verify list and input"):
        view_vmr_page.open_and_verify_art_no_dropdown()

    with allure.step("Click on Status filter drop down and verify order status options"):
        view_vmr_page.open_and_verify_status_dropdown()

@allure.story("Verify that the table should display the all the columns in view order proposal screen")
@allure.story("Verify that the View button is display in the View VMR Proposal screen")
@pytest.mark.parametrize("data", TEST_ECIS_VIEW_VMR_PROPOSAL_COLUMNS)
def test_ecis_view_vmr_proposal_columns(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Open File Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()

    with allure.step("Click on 'View VMR Proposal'"):
        dashboard_page.select_view_vmr_proposal()

    with allure.step("Click on 'Find' Button"):
        view_vmr_page.click_find()

    with allure.step("Verify the column are displayed in the View VMR Proposal screen"):
        view_vmr_page.verify_column_displayed()

    with allure.step("Verify that the View button is display in the View VMR Proposal screen"):
        view_vmr_page.verify_view_button()

@allure.story("Verify that the system displays the popup window with VMR order details with the numbers and those details will be separate with Comma")
@allure.story("Verify that the Find and clear buttons are available")
@pytest.mark.parametrize("data", TEST_VMR_VIEW_FLOW)
def test_vmr_view_flow(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Select file menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()

    with allure.step("Select VMR Proposal Search"):
        view_vmr_page.open_vmr_proposal()
        view_vmr_page.search_order()

    with allure.step("Popup"):
        popup = view_vmr_page.open_order_details_popup()
        view_vmr_page.validate_order_popup_details(popup)

    with allure.step("Clear"):
        view_vmr_page.clear_search()
        view_vmr_page.apply_receiver_and_order_filters()

@allure.story("Verify that the order details are display based on the search condition while click on find")
@allure.story("Verify that the select filters are removed while clicking on clear button")
@allure.story("Verify that the order should be display in Created status if the ECIS_VMR_ORD_PROP_H_T .ORD_PROP_CRE_DATE column value is not Null.")
@pytest.mark.parametrize("data", TEST_FIND_AND_CLEAR)
def test_find_and_clear(ecis_dashboard_page,data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page

    vmr_order_ref = data["vmr_order_ref"]

    with allure.step("Select database and supplier"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Navigate to View VMR Proposal"):
        dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()
        view_vmr_page.open_vmr_proposal()

    with allure.step("Apply filter and search"):
        view_vmr_page.apply_order_ref_filter(vmr_order_ref)

    with allure.step("Verify order ref in results"):
        view_vmr_page.verify_order_ref_in_results(vmr_order_ref)

    with allure.step("Verify Sent Proposal status for the order"):
        view_vmr_page.verify_sent_proposal_status_for_order(vmr_order_ref)

    with allure.step("Verify Sent Proposal status for the order"):
        # vmr_find_clear_page.verify_sent_proposal_is_visible()
        view_vmr_page.verify_sent_proposal_status_for_order(vmr_order_ref)

    with allure.step("Clear search filters"):
        view_vmr_page.clear_search()

@allure.story("TC05 - Uploading Invalid Orders Document")
@pytest.mark.parametrize("data", TEST_ECIS_VMR_UPLOAD)
def test_ecis_vmr_upload(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select supplier and database"):

        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Open File Menu"):
        # dashboard_page.dashboard_page()
        dashboard_page.click_menu_file()

    with allure.step("Open VMR Order"):
        create_vmr_page.open_vmr_order()

    with allure.step("Select VMR order upload"):
        create_vmr_page.select_vmr_order_upload()

    with allure.step("Select Upload VMR Orders"):
        create_vmr_page.select_upload_vmr_orders()

    with allure.step("Browse and upload VMR Excel from testdata folder"):
        # Uses static testdata/demo1.xls internally
        create_vmr_page.browse_and_upload_file()

    with allure.step("Click Start Upload"):
        create_vmr_page.click_start_upload()

    with allure.step("Handle invalid orders popup if shown"):
        create_vmr_page.handle_invalid_orders_popup()

@allure.story("TC03 - Bulk upload with same supplier and same RCV")
@pytest.mark.parametrize("data", TEST_ECIS_CREATE_VMR_DIFFERENT_RCV_ARTICLE_BULK_UPLOAD)
def test_ecis_create_same_supplier_rcv_bulk_upload(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
     # -------------------- Step 1 --------------------
    with allure.step("Step 1: Login and select supplier & database"):

            ecis_welcome_page.select_supplier(data["supplier"])
            ecis_welcome_page.click_continue()

    # -------------------- Step 2 --------------------
    with allure.step("Step 2: Open Create VMR Order from File menu"):
            dashboard_page.dashboard_page()
            dashboard_page.click_menu_file()
            create_vmr_page.open_vmr_order()

        # -------------------- Step 3 --------------------
    with allure.step("Step 4: Select VMR Order Upload option"):
            create_vmr_page.select_vmr_order_upload()

        # -------------------- Step 4 --------------------
    with allure.step("Step 5: Download VMR upload template"):
            create_vmr_page.select_download_and_confirm()
            create_vmr_page.click_download_button()
            create_vmr_page.verify_file_downloaded("Upload_File")
    with allure.step("Step 3: Select close download popup"):
        create_vmr_page.close_download_popup()

        with allure.step("Step 6: Switch back to Upload VMR Orders mode"):
            create_vmr_page.select_upload_vmr_orders()

        # -------------------- Step 6 --------------------
        with allure.step("Browse and upload VMR Excel from testdata folder"):
            # Uses static testdata/vmr3.xls internally
            create_vmr_page.browse_and_upload_file_same_rcv()
        # -------------------- Step 7 --------------------
        with allure.step("Step 8: Start upload and handle success popup"):
            create_vmr_page.click_start_upload()


@allure.story("TC04 - Bulk upload with different RCV and Article combinations")
@pytest.mark.parametrize("data",TEST_ECIS_CREATE_VMR_DIFFERENT_RCV_ARTICLE_BULK_UPLOAD)
def test_ecis_create_vmr_different_rcv_article_bulk_upload(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page

        # -------------------- Step 1 --------------------
    with allure.step("Step 1: Login and select supplier & database"):
            ecis_welcome_page.select_supplier(data["supplier"])
            ecis_welcome_page.click_continue()

        # -------------------- Step 2 --------------------
    with allure.step("Step 2: Open Create VMR Order from File menu"):
            dashboard_page.dashboard_page()
            dashboard_page.click_menu_file()
            create_vmr_page.open_vmr_order()

        # -------------------- Step 3 --------------------
    with allure.step("Step 3: Select VMR Order Upload option"):
            create_vmr_page.select_vmr_order_upload()

        # -------------------- Step 4 --------------------
    with allure.step("Step 4: Download VMR upload template"):
        create_vmr_page.select_download_and_confirm()
        create_vmr_page.click_download_button()
        create_vmr_page.verify_file_downloaded("Upload_File")
    with allure.step("Step 3: Select close download popup"):
        create_vmr_page.close_download_popup()

        # -------------------- Step 5 --------------------
        with allure.step("Step 5: Select Upload VMR Orders"):
            create_vmr_page.select_upload_vmr_orders()

        # -------------------- Step 6 --------------------
        with allure.step("Browse and upload VMR Excel from testdata folder"):
            create_vmr_page.browse_and_upload_diff_file()

        # -------------------- Step 7 --------------------
        with allure.step("Step 7: Start upload file"):
            create_vmr_page.click_start_upload()

@allure.story("TC09-Verify RCV Code, RCV Type, End RCV Code, End RCV Type exist in grid")
@pytest.mark.parametrize("data", TEST_VERIFY_RCV_COLUMNS)
def test_verify_rcv_and_end_rcv_columns_in_result_grid(ecis_dashboard_page,data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Step 1: Login and select supplier & database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Validate ECIS dashboard is loaded"):
        dashboard_page.dashboard_page()

    with allure.step("Navigate to File → View VMR Order Proposal"):
                # dashboard_page.click_menu_file()
        dashboard_page.select_view_vmr_proposal()

    with allure.step("Select one filter (VMR Order Ref OR Art No)"):
        view_vmr_page.open_and_verify_vmr_order_ref_dropdown(data["order_no"])

    with allure.step("Click Find"):
        view_vmr_page.click_find()

    with allure.step("Verify result grid data and RCV columns"):
        view_vmr_page.verify_result_grid_contains_expected_data(data["order_no"])
        view_vmr_page.verify_rcv_columns_in_grid()

@allure.story("Verify Export File downloads VMR order proposal data successfully")
@pytest.mark.parametrize("data", TEST_VERIFY_EXPORT_FILE)
def test_verify_export_file(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Step 1: Login and select supplier & database"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

    with allure.step("Navigate to View VMR Order Proposal"):
        # dashboard_page.click_menu_file()
        dashboard_page.select_view_vmr_proposal()

    with allure.step("Select VMR Order Ref and click Find"):
        view_vmr_page.open_and_verify_vmr_order_ref_dropdown(data["order_no"])
        view_vmr_page.click_find()
        # view_vmr_page.select_first_vmr_row()

    with allure.step("Export VMR Order Proposal file"):
        file_name = view_vmr_page.export_vmr_order_proposal()

    assert file_name.endswith(".txt")

@allure.story("Verify copy clip is visible and Copies displayed VMR data")
@pytest.mark.parametrize("data", TEST_VERIFY_ORDER_STATUS_SENT_PROPOSAL)
def test_verify_copy_clip_and_copied_file_export(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Login to ECIS application"):
        ecis_welcome_page.select_supplier(data["supplier"])
        ecis_welcome_page.click_continue()

        with allure.step("Navigate to View VMR Order Proposal"):
            dashboard_page.select_view_vmr_proposal()

        with allure.step("Select VMR Order Ref and click Find"):
            view_vmr_page.open_and_verify_vmr_order_ref_dropdown(data["order_no"])
            view_vmr_page.click_find()




@allure.story("Verify order status is Sent Proposal")
@pytest.mark.parametrize("data", TEST_VERIFY_ORDER_STATUS_SENT_PROPOSAL)
def test_verify_order_status_sent_proposal(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page

    with allure.step("Login to ECIS application"):

            ecis_welcome_page.select_supplier(data["supplier"])
            ecis_welcome_page.click_continue()
            dashboard_page.dashboard_page()

    with allure.step("Navigate to Create VMR Proposal screen"):
        dashboard_page.page.get_by_text("File Create VMR Proposal View").click()
        dashboard_page.page.get_by_role("link", name="Create VMR Proposal").click()
        create_vmr_page.create_order_proposal_vmr()

        # Dialog handler now comes from page file
        create_vmr_page.page.once(
            "dialog",
            view_vmr_page.handle_vmr_creation_dialog
        )

    with allure.step("Create VMR order proposal"):
            create_vmr_page.select_receiver()
            create_vmr_page.enter_plan_date()
            create_vmr_page.select_article_no()
            create_vmr_page.enter_proposed_qty("10")
            create_vmr_page.click_add_article()
            create_vmr_page.create_order_total_pallet_and_verify()

        # Assertion moved to page file
    view_vmr_page.validate_vmr_order_reference()

    with allure.step("Navigate to View VMR Order Proposal"):
            dashboard_page.select_view_vmr_proposal()

    with allure.step("Filter created order and click Find"):
            view_vmr_page.open_and_verify_vmr_order_ref_dropdown(
                data["order_no"]
            )
            view_vmr_page.click_find()

    with allure.step("Verify order status is Sent Proposal"):
            view_vmr_page.verify_order_status_sent_proposal(data["order_no"])
