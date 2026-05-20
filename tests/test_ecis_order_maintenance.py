import pytest
import allure
from testdata.ecis_order_maintenance_data import (TEST_ORDER_MAINTENANCE_CANCELLATIONS)
from testdata.ecis_order_maintenance_data import (TEST_ORDER_MAINTENANCE_MOVE)
from testdata.ecis_order_maintenance_data import (TEST_ORDER_MAINTENANCE_DWP_KEY)
from testdata.ecis_order_maintenance_data import (TEST_VERIFY_EXPORT_FILE_DATA)
from testdata.ecis_order_maintenance_data import (TEST_VERIFY_COPY_CLIP_DATA)
from testdata.ecis_order_maintenance_data import(TEST_BLOCKED_ORDER_POPUP)
from testdata.ecis_order_maintenance_data import(TEST_VALIDATE_CANCELLED_ORDER)

@allure.feature("Order Maintenance")
@allure.story(
    "Verify that the rason code must be mandatory for supplier-initiated cancellations for OFP orders (excl. DDC order types)")
@pytest.mark.parametrize("test_data",TEST_ORDER_MAINTENANCE_CANCELLATIONS)
def test_ecis_order_maintenance_cancellations(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("verify the order maintenance header page"):
        order_maintenance_page.verify_order_maintenance_header()

    with allure.step("select the order type ZVMR/ZNB "):
        order_maintenance_page.select_order_type(test_data["otype"])

    with allure.step("click on find button"):
        order_maintenance_page.click_find_button()

    with allure.step("select the order form the grid"):
        order_maintenance_page.select_order_from_grid(test_data["onumber"])

    with allure.step(
            "Select the order line and click on cancel selected lines button and verify the error message"):
        order_maintenance_page.click_cancel_button()

    with allure.step("Search that order and select it and click on confirm button"):
        order_maintenance_page.search_order_confirm(test_data["onumber"])

    with allure.step("click on confirm button"):
        order_maintenance_page.click_confirm_button()



@allure.story(
    "TC03: Verify that the reason code must not be mandatory(optional) for supplier-initiated PO confirmation updates(Move) (change of date) ")
@pytest.mark.parametrize("test_data",TEST_ORDER_MAINTENANCE_MOVE)
def test_ecis_order_maintenance_move(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("verify the order maintenance header page"):
        order_maintenance_page.verify_order_maintenance_header()

    with allure.step("select the order type ZVMR/ZNB "):
        order_maintenance_page.select_order_type(test_data["otype"])

    with allure.step("click on find button"):
        order_maintenance_page.click_find_button()

    with allure.step("select the order form the grid"):
        order_maintenance_page.select_order_from_grid(test_data["onumber"])

    with allure.step("Select the order line and click on move  button and verify the error message"):
        order_maintenance_page.click_move_button()

    with allure.step("Order will be move to new date with status pending"):
        order_maintenance_page.verify_pending_status(test_data["onumber"])


@allure.story(
    "Verify that the reason code must not be mandatory(optional) for supplier-initiated PO confirmation updates (DWP key)  (excl. DDC order types) ")
@pytest.mark.parametrize("test_data",TEST_ORDER_MAINTENANCE_DWP_KEY)
def test_ecis_order_maintenance_dwp_key(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("verify the order maintenance header page"):
        order_maintenance_page.verify_order_maintenance_header()

    with allure.step("select the order type ZVMR/ZNB "):
        order_maintenance_page.select_order_type(test_data["otype"])

    with allure.step("click on find button"):
        order_maintenance_page.click_find_button()

    with allure.step("select the order form the grid"):
        order_maintenance_page.select_order_from_grid(test_data["onumber"])

    with allure.step("Select the order line and click on change button "):
        order_maintenance_page.click_change_button()


@allure.story("Verify, To block purchase order update(confirm, reconfirm, Move or cancel) of the order line in Order Maintenance screen")
@pytest.mark.parametrize("test_data",TEST_BLOCKED_ORDER_POPUP)
def test_blocked_order_popup_handling(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select database and supplier"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("Selecting S from dropdown"):
        order_maintenance_page.select_delivery_status_s()
        order_maintenance_page.click_find_button()
        order_maintenance_page.select_first_order()

    with allure.step("Handling Popup of Order maintenance"):
        # Separate validations
        order_maintenance_page.click_confirm_and_validate_popup()
        order_maintenance_page.click_move_and_validate_popup()
        order_maintenance_page.click_change_and_validate_popup()


@allure.story("Verify, the order line in Order Maintenance screen, which has the DELETE_FLAG as 'L'")
@pytest.mark.parametrize("test_data",TEST_VALIDATE_CANCELLED_ORDER)
def test_validate_cancelled_order_status(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step("Select database and supplier"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("Selecting L from dropdown"):
        order_maintenance_page.select_all_orders()
        order_maintenance_page.select_deletion_indicator_l()
        order_maintenance_page.click_find_button()

    with allure.step("Handling Status of Order maintenance"):
        order_maintenance_page.validate_order_status_cancelled()


@allure.story("Verify the export file button is working")
@pytest.mark.parametrize("test_data",TEST_VERIFY_EXPORT_FILE_DATA)
def test_verify_export_file(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("verify the order maintenance header page"):
        order_maintenance_page.verify_order_maintenance_header()

    with allure.step("click on find button"):
        order_maintenance_page.click_find_button()

    with allure.step("Export order maintenance file"):
        order_maintenance_page.verify_export_order_maintenance_file()


@allure.story("Verify the Copyclip button is working with this new column.")
@pytest.mark.parametrize("test_data",TEST_VERIFY_COPY_CLIP_DATA)
def test_verify_copyclip(ecis_dashboard_page,test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        create_vmr_page,
        view_vmr_page,
        order_maintenance_page,
        *_,
    ) = ecis_dashboard_page
    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Open Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on order menu"):
        order_maintenance_page.click_order_link()

    with allure.step("verify the order maintenance header page"):
        order_maintenance_page.verify_order_maintenance_header()
    with allure.step("Click Find button"):
        order_maintenance_page.click_find_button()

    with allure.step("Verify CopyClip and save copied data"):
        order_maintenance_page.verify_copyclip_and_save_data()