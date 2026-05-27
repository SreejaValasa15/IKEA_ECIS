import pytest
import allure
from testdata.ecis_consignment_report_data import CONSIGNMENT_TEST_DATA
from testdata.ecis_consignment_report_data import CONSIGNMENT_TEST_INVOICE
from testdata.ecis_consignment_report_data import CONSIGNMENT_TEST_DATA_FOR_DDC_OR_COS

@allure.story("Consignment information report")
@pytest.mark.parametrize( "data",
    CONSIGNMENT_TEST_DATA,
    ids=[
        f"{d['report_name']} | {d['consignment_id']} | {d['export_type']}"
        for d in CONSIGNMENT_TEST_DATA
    ]
)
def test_consignment_report(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
        consignment_report_page,
    ) = ecis_dashboard_page

    print(
        f"\nExecuting: {data['report_name']} | "
        f"{data['consignment_id']} | {data['export_type']}"
    )

    # -------- LOGIN --------
    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    # -------- CONSIGNMENT --------
    with allure.step("Navigate to consignment and select record"):
        consignment_report_page.open_consignment()
        consignment_report_page.select_checkbox(data["consignment_id"])

        booking_popup = consignment_report_page.click_view()

    #  -------- PHASE 1: PREVIEW BEFORE CHANGES --------
    with allure.step("Preview BEFORE LU change"):
        consignment_report_page.preview_report_and_close(
            booking_popup,
            data["report_name"]
        )

    # -------- APPLY BOOKING CHANGES --------
    with allure.step("Modify booking details and save"):
        consignment_report_page.perform_booking(
            booking_popup,
            lu_type=data["lu_type"],
            booking_name=data["booking_name"]
        )

    # -------- GENERATE REPORT AFTER CHANGES ---------------
    with (allure.step("Generate report after changes")):
        report_popup = consignment_report_page.open_reports(booking_popup)
        consignment_report_page.select_report(
            report_popup,
            data["report_name"]
        )
        consignment_report_page.select_consignment_report(report_popup)

        print_popup = consignment_report_page.show_report(report_popup)

    # -------- PRINT & EXPORT --------
    with allure.step("Print and export report"):
        consignment_report_page.print_report(print_popup)

        download = consignment_report_page.export_report(
            print_popup,
            report_popup,
            booking_popup,
            file_type=data["export_type"]
        )

    # -------- VALIDATION --------
    with allure.step("Validate report download"):
        assert download is not None

@allure.story("Consignment information report for Invoice related reports")
@pytest.mark.parametrize( "data",
    CONSIGNMENT_TEST_INVOICE,
    ids=[
        f"{d['report_name']} | {d['consignment_id']} | {d['export_type']}"
        for d in CONSIGNMENT_TEST_INVOICE
    ]
)
def test_consignment_invoice_flow(ecis_dashboard_page, data):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
        consignment_report_page,
    ) = ecis_dashboard_page
    print(
        f"\nExecuting: {data['report_name']} | "
        f"{data['consignment_id']} | {data['export_type']}"
    )

    # -------- LOGIN --------
    with allure.step("Select supplier and database"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    # -------- CONSIGNMENT --------
    with allure.step("Navigate to consignment and select record"):
        consignment_report_page.open_consignment()
        consignment_report_page.select_checkbox(data["consignment_id"])

        booking_popup = consignment_report_page.click_view()

    # -------- PHASE 1: PREVIEW BEFORE CHANGES --------
    with allure.step("Preview BEFORE LU change"):
        report_popup = consignment_report_page.open_reports(booking_popup)

        consignment_report_page.select_report(
            report_popup,
            data["report_name"]
        )

        preview_page = consignment_report_page.show_report(report_popup)
        preview_page.close()
        report_popup.close()

    # ---------- INVOICE FLOW ----------
    with allure.step("Open invoice page"):
        invoice_page = consignment_report_page.open_invoice(booking_popup)

    with allure.step(f"Set invoice date: {data['invoice_date']}"):
        consignment_report_page.set_invoice_date(
            invoice_page, data["invoice_date"]
        )

    # ---------- INVOICE REPORTS ----------
    with allure.step("Open invoice reports"):
        invoice_reports_page = consignment_report_page.open_reports(invoice_page)

    with allure.step("Generate invoice report"):
        invoice_preview = consignment_report_page.show_report(invoice_reports_page)

    # -------- PRINT & EXPORT --------
    with allure.step("Print and export report"):
        consignment_report_page.print_report(invoice_preview)

        download = consignment_report_page.export_report(
            invoice_preview,
            report_popup,
            booking_popup,
            file_type=data["export_type"]
        )

    # -------- VALIDATION --------
    with allure.step("Validate report download"):
        assert download is not None

    # -------- CLEANUP --------
    with allure.step("Close all open pages"):
        invoice_preview.close()
        booking_popup.close()

@allure.story("Consignment information report for DDC or COS related reports")
@pytest.mark.parametrize( "data",
    CONSIGNMENT_TEST_DATA_FOR_DDC_OR_COS,
    ids=[
        f"{d['report_name']} | {d['consignment_id']} | {d['export_type']}"
        for d in  CONSIGNMENT_TEST_DATA_FOR_DDC_OR_COS
    ]
)
def test_consignment_report_label_DDC_or_COS_report(ecis_dashboard_page,data ):
    (
        dashboard_page,
        ecis_welcome_page,
        *_,
        ecis_consignment_page,
        ecis_order_report_page,
        consignment_report_page,
    ) = ecis_dashboard_page

    # -------- LOGIN --------
    with allure.step("Select supplier"):
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    # -------- CONSIGNMENT --------
    with allure.step("Select consignment"):
        consignment_report_page.open_consignment()
        consignment_report_page.select_checkbox(data["consignment_id"])

        booking_popup = consignment_report_page.click_view()

    # -------- BEFORE CHANGE --------
    with allure.step("Preview BEFORE LU change"):
        consignment_report_page.preview_find_select_all(
            booking_popup,
            data["report_name"]
        )

    # -------- APPLY LU TYPE CHANGE --------
    with allure.step("Modify LU Type"):
        consignment_report_page.perform_booking(
            booking_popup,
            lu_type=data["lu_type"],
            booking_name=data["booking_name"]
        )

    # -------- AFTER CHANGE --------
    with allure.step("Generate report AFTER change"):
        report_popup = consignment_report_page.open_reports(booking_popup)

        consignment_report_page.select_report(
            report_popup,
            data["report_name"]
        )

        consignment_report_page.find_and_select_all(report_popup)

        print_popup = consignment_report_page.show_report(report_popup)

    # -------- EXPORT --------
    with allure.step("Export report"):
        consignment_report_page.print_report(print_popup)

        download = consignment_report_page.export_report(
            print_popup,
            report_popup,
            booking_popup,
            file_type=data["export_type"]
        )

    # -------- VALIDATION --------
    with allure.step("Validate download"):
        assert download is not None












