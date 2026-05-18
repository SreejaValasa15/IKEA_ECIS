import pytest
import allure

from testdata.ecis_order_maintenance_report_data import (TEST_ORDER_REPORTS_MATRIX)
from testdata.ecis_order_maintenance_report_data import (TEST_SAVE_ORDER_REPORT)
@allure.feature("Reports")
@allure.story("Show as Matrix functionality")
@pytest.mark.parametrize("test_data", TEST_ORDER_REPORTS_MATRIX)
def test_order_reports_matrix(ecis_dashboard_page,test_data):
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
def test_save_order_report(ecis_dashboard_page,test_data):
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


