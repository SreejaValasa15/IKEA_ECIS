TEST_CONSIGNMENT_REPORT_PACKING_LABEL_FOR_DDC_OR_COS = [
    {
        "scode": "22569",
        "consignment_id": "ECIS33489",
        "report_name": "Packing Label for DDC/COS",
        "lu_type": "1M",
        "booking_name": "Transport Booking",
        "export_type": "pdf"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33588",
        "report_name": "Packing Label for DDC/COS",
        "lu_type": "C31-6, Container; 6 tons (SA)",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    }
]
TEST_CONSIGNMENT_REPORT_TRANSPORT = [
    {
        "scode": "22569",
        "consignment_id": "ECIS33489",
        "report_name": "Transport Booking",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "pdf"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33588",
        "report_name": "Transport Booking",
        "lu_type": "1M",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33485",
        "report_name": "Transport Booking",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    }
]
TEST_CONSIGNMENT_REPORT_CI=[
    {
        "scode": "22569",
        "consignment_id": "ECIS33489",
        "report_name": "Consignment Information",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "pdf"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33489",
        "report_name": "Consignment Information",
        "lu_type": "1M",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    }

]
TEST_CONSIGNMENT_REPORT_CI_FOR_DDC_OR_COS=[
    {
        "scode": "22569",
        "consignment_id": "ECIS33489",
        "report_name": "Consignment information for DDC/COS",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "pdf"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33485",
        "report_name": "Consignment information for DDC/COS",
        "lu_type": "1M",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    }

]
#-----------------------------
TEST_CONSIGNMENT_REPORT_PACKING_LIST_2_ARTICLE_LEVEL= [
    {
        "scode": "22569",
        "consignment_id": "ECIS33489",
        "report_name": "Packing List 2, Article Level (Importer Russia)",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "pdf"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33588",
        "report_name": "Packing List 2, Article Level (Importer Russia",
        "lu_type": "1M",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    },
    {
        "scode": "22569",
        "consignment_id": "ECIS33485",
        "report_name": "Packing List 2, Article Level (Importer Russia)",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "excel"
    }
]
TEST_CONSIGNMENT_REPORT_PACKING_LIST_3_ARTICLE_LEVEL=[
{
    "scode": "22569",
    "consignment_id": "ECIS33485",
    "report_name": "Packing List 3 - For loadings with transit orders",
    "lu_type": "AP-LCL",
    "booking_name": "Transport Booking",
    "export_type": "excel"
},
{
    "scode": "15653",
    "consignment_id": "ECIS218110",
    "report_name": "Packing List 3 - For loadings with transit orders",
    "lu_type": "1M",
    "booking_name": "Transport Booking",
     "export_type": "pdf"
}]

TEST_CONSIGNMENT_REPORT_CONSIGNMENT_INFO_MHS = [{
        "scode": "22569",
        "consignment_id": " ECIS33489",
        "report_name": "Consignment information MHS",
        "lu_type": "AP-LCL",
        "booking_name": "Transport Booking",
        "export_type": "excel"
}]

TEST_STATEMENT_OF_COMPLIANCE=[
{
    "scode": "22569",
    "consignment_id": " ECIS33489",
    "status": "Trp Conf",
    "report_name": "Statement of compliance",
    "invoice_date": "15",
    "export_type": "excel"
},
{
    "scode": "22569",
    "consignment_id": " ECIS33489",
    "status": "Trp Conf",
    "report_name": "Statement of compliance",
    "invoice_date": "16",
    "export_type": "pdf"
}
]
INVOICE_AGGREGATED_PO_NUMBER=[
{
    "scode": "22569",
    "consignment_id": " ECIS33489",
    "status": "Trp Conf",
    "report_name": "Invoice - aggregated PO number",
    "invoice_date": "16",
    "export_type": "pdf"
},
{
    "scode": "22569",
    "consignment_id": " ECIS33489",
    "status": "Trp Conf",
    "report_name": "Invoice - aggregated PO number",
    "invoice_date": "17",
    "export_type": "excel"
}
]


INVOICE_ITEMIZED_ON_PO_LINE=[
{
    "scode": "22569",
    "consignment_id": " ECIS33489",
    "status": "Trp Conf",
    "report_name": "Invoice - itemized on PO line",
    "invoice_date": "16",
    "export_type": "pdf"
},
{
    "scode": "22569",
    "consignment_id": " ECIS33489",
    "status": "Trp Conf",
    "report_name": "Invoice - itemized on PO line",
    "invoice_date": "17",
    "export_type": "excel"
}

]
CONSIGNMENT_TEST_DATA = (
    # TEST_CONSIGNMENT_REPORT_CONSIGNMENT_INFO_MHS+
    # TEST_CONSIGNMENT_REPORT_TRANSPORT +
    # TEST_CONSIGNMENT_REPORT_CI+
    # TEST_CONSIGNMENT_REPORT_PACKING_LIST_2_ARTICLE_LEVEL+
    TEST_CONSIGNMENT_REPORT_PACKING_LIST_3_ARTICLE_LEVEL
)
CONSIGNMENT_TEST_DATA_FOR_DDC_OR_COS = (
TEST_CONSIGNMENT_REPORT_CI_FOR_DDC_OR_COS+
TEST_CONSIGNMENT_REPORT_PACKING_LABEL_FOR_DDC_OR_COS
)

CONSIGNMENT_TEST_INVOICE = (
TEST_STATEMENT_OF_COMPLIANCE+
INVOICE_AGGREGATED_PO_NUMBER+
INVOICE_ITEMIZED_ON_PO_LINE

)
