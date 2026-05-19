
import pytest
import allure
from pygments.lexers import data

from testdata.ecis_order_maintenance_report_data import (TEST_REPORT_EXPORT)
from testdata.ecis_order_maintenance_report_data import (TEST_COPY_CLIP)
from testdata.ecis_order_maintenance_report_data import (TEST_PRINT_AND_DOWNLOAD)

from testdata.ecis_order_maintenance_report_data import (TEST_ORDER_REPORTS_MATRIX)
from testdata.ecis_order_maintenance_report_data import (TEST_SAVE_ORDER_REPORT)
from testdata.ecis_order_maintenance_report_data import (TEST_REPORT)
from testdata.ecis_order_maintenance_report_data import (TEST_ORDER_REPORT_SEARCH)


@allure.feature("Dashboard - Copy Clip")
@pytest.mark.parametrize("test_data", TEST_COPY_CLIP)
def test_copy_clip(ecis_dashboard_page, test_data):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page

    ) = ecis_dashboard_page

    with allure.step("Select the database and supplier"):
        dashboard_page.select_database(test_data["database"])
        dashboard_page.select_supplier(test_data["scode"])
        dashboard_page.click_continue()

    with allure.step("Navigate to Order Report"):
        ecis_order_report_page.go_to_reports()
        ecis_order_report_page.go_to_order()

    with allure.step("Open Copy Clip and interact"):
        ecis_order_report_page.open_copy_clip()
        ecis_order_report_page.interact_with_iframe()

    with allure.step("Close popup"):
        ecis_order_report_page.close_iframe()


# ------------------------------------------------------------

@allure.feature("Report - Print and Download")
@pytest.mark.parametrize("test_data", TEST_PRINT_AND_DOWNLOAD)
def test_print_and_download(ecis_dashboard_page, test_data):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
    ) = ecis_dashboard_page

    with allure.step("Select database and supplier"):
        dashboard_page.select_database(test_data["database"])
        dashboard_page.select_supplier(test_data["scode"])
        dashboard_page.click_continue()

    with allure.step("Navigate to Order Report"):
        ecis_order_report_page.go_to_reports()
        ecis_order_report_page.go_to_order()

    with allure.step("Open print popup"):
        ecis_order_report_page.open_print_popup()

    with allure.step("Print report"):
        ecis_order_report_page.print_report()

    with allure.step("Export report"):
        ecis_order_report_page.export_report()


# ------------------------------------------------------------

@allure.feature("Report Export")
# @pytest.mark.parametrize("export_type", ["PDF","Microsoft Excel(XLS)"])
@pytest.mark.parametrize("export_type", TEST_REPORT_EXPORT)
def test_report_export(ecis_dashboard_page, export_type):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
    ) = ecis_dashboard_page

    with allure.step("Select database and supplier"):
        dashboard_page.select_database(export_type["database"])
        dashboard_page.select_supplier(export_type["scode"])
        dashboard_page.click_continue()

    with allure.step("Navigate to Order Report"):
        ecis_order_report_page.go_to_reports()
        ecis_order_report_page.go_to_order()

    with allure.step("Open print popup"):
        ecis_order_report_page.open_print_popup()

    with allure.step(f"Export report as {export_type}"):
        download = ecis_order_report_page.export_pdf_report(export_type["export_option"])

    with allure.step("Validate download"):
        assert download is not None
        print(f"{export_type} downloaded: {download.suggested_filename}")

    with allure.step("Close popup"):
        ecis_order_report_page.close_popup()


@allure.feature("Reports")
@allure.story("Show as Matrix functionality")
@pytest.mark.parametrize("test_data", TEST_ORDER_REPORTS_MATRIX)
def test_order_reports_matrix(ecis_dashboard_page, test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        *_,
        ecis_order_report_page
    ) = ecis_dashboard_page

    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Reports Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_reports()

    with allure.step("Click on order report on ECIS menu screen"):
        ecis_order_report_page.navigate_to_order_reports()

    with allure.step("Select the order under the Report Tab and click on Find button"):
        ecis_order_report_page.click_on_order_report()


@allure.story("Save functionality")
@pytest.mark.parametrize("test_data", TEST_SAVE_ORDER_REPORT)
def test_save_order_report(ecis_dashboard_page, test_data):
    (
        ecis_welcome_page,
        dashboard_page,
        *_,
        ecis_order_report_page
    ) = ecis_dashboard_page

    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(test_data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Reports Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_reports()

    with allure.step("Click on order report on ECIS menu screen"):
        ecis_order_report_page.navigate_to_order_reports()

    with allure.step("Click on clear column button"):
        ecis_order_report_page.click_on_clear_button()

    with allure.step("Click on show column selection button"):
        ecis_order_report_page.click_column_selection_button()

    with allure.step("Generate new query"):
        for dropdown, option in test_data["dropdown_data"]:
            ecis_order_report_page.select_option_by_text(dropdown, option)

    with allure.step("click on find button"):
        ecis_order_report_page.click_on_find_button()

    with allure.step("Click on 'Maintain Queries' button"):
        ecis_order_report_page.click_on_maintain_queries_button(test_data["query_name"])

@allure.story("Verify the order report export file flow is working")
@pytest.mark.parametrize("test_data", TEST_REPORT)
def test_verify_order_report_export(ecis_dashboard_page,test_data):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
    ) = ecis_dashboard_page

    with allure.step("Select supplier"):
        dashboard_page.select_supplier(test_data["supplier"])
        dashboard_page.click_continue()

    with allure.step("Navigate to Order Report"):
        ecis_order_report_page.navigate_to_order()

    with allure.step("Click on Find button"):
        ecis_order_report_page.click_find_button()

    with allure.step("Export order report file"):
        ecis_order_report_page.export_order_report_file()


@allure.feature("Order Report Search operations")
@pytest.mark.parametrize("data", TEST_ORDER_REPORT_SEARCH)
def test_verify_order_report_search_operations(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
    ) = ecis_dashboard_page

    with allure.step("Select supplier and database"):
        dashboard_page.select_supplier(data["scode"])
        dashboard_page.click_continue()

    with allure.step("Navigate to Order Report"):
        ecis_order_report_page.navigate_to_order()

    with allure.step("Click on find button"):
        ecis_order_report_page.click_find_button()
    with allure.step("Perform search"):
        ecis_order_report_page.search_order_report(data)

    with allure.step("Validate results"):
        ecis_order_report_page.validate_search_results()