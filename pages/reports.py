import streamlit as st
import pandas as pd
from datetime import date
import io
from utils.pdf_generator import generate_daily_report_pdf   
from db.queries import (
    get_daily_report,
    get_employee_performance
)

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title("Reports")

tab1, tab2 = st.tabs(
    [
        "Daily Report",
        "Employee Performance"
    ]
)

# ---------------------------
# Daily Report
# ---------------------------

with tab1:

    report_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    rows = get_daily_report(
        report_date
    )

    df = pd.DataFrame(
        rows,
        columns=[
            "Employee",
            "Category",
            "Service",
            "Activity Location",
            "Activity",
            "Status"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------------------
# Employee Performance
# ---------------------------

with tab2:

    rows = get_employee_performance()

    df = pd.DataFrame(
        rows,
        columns=[
            "Employee",
            "Total Logs"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

output = io.BytesIO()

with pd.ExcelWriter(
        output,
        engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False
    )

st.download_button(
    label="Download Excel",
    data=output.getvalue(),
    file_name="daily_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


pdf_file = generate_daily_report_pdf(
    rows,
    "daily_report.pdf"
)

with open(pdf_file, "rb") as f:

    st.download_button(
        "Download PDF Report",
        f,
        file_name="daily_report.pdf",
        mime="application/pdf"
    )