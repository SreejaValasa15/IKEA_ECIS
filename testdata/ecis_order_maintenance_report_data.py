TEST_REPORT=[{
    "supplier":"50029"
},
{
    "supplier":"23231",
}]
TEST_ORDER_REPORT_SEARCH = [
    {
        "database": "Production",
        "scode": "50029",
        "rcv": "1406 - LSC",
        "order_type": "L",
        "art_no": "00517060"
    },
    {
        "database": "Production",
        "scode": "50029",
        "rcv": "1441 - LSC",
        "order_type": "L",
        "art_no": "00517098"
    },
    {
        "database": "Production",
        "scode": "50029",
        "rcv": "1573 - LSC",
        "order_type": "L",
        "art_no": "00517060"
    }
]
TEST_COPY_CLIP =[
    {
        "database": "Production",
        "scode": "15653",
    }
]

TEST_PRINT_AND_DOWNLOAD =[
    {
        "database": "Production",
        "scode": "15653",
    }
]

TEST_REPORT_EXPORT = [ {
    "database": "Production",
     "scode": "15653",
     "export_option":"PDF"
},
    {
        "database": "Production",
        "scode": "15653",
    "export_option":"Microsoft Excel(XLS)"
    }
]

TEST_ORDER_REPORTS_MATRIX =[
    {
         "scode": "23231",
    }]
TEST_SAVE_ORDER_REPORT =[
    {
        "scode": "23231",
        "dropdown_data": [
            ("Main", "Ord Status"),
            ("Reference", "Order No 2"),
            ("Customer Info", "Customer Name"),
            ("Date", "Rcv Date"),
            ],
        "query_name":"Order Report"
    }]

