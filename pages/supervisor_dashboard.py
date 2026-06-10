import streamlit as st
import pandas as pd

from db.queries import (
    get_supervisor_dashboard,
    get_top_employees,
    get_status_summary
)

# ----------------------------------
# Session Check
# ----------------------------------

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ----------------------------------
# Role Check
# ----------------------------------

if st.session_state["role"] not in [
    "ADMIN",
    "SUPERVISOR"
]:
    st.error("Access Denied")
    st.stop()

# ----------------------------------
# Page Title
# ----------------------------------

st.title("Supervisor Dashboard")

# ----------------------------------
# KPI Cards
# ----------------------------------

counts = get_supervisor_dashboard()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Pending Approvals",
        counts[0]
    )

with col2:
    st.metric(
        "Approved Logs",
        counts[1]
    )

with col3:
    st.metric(
        "Rejected Logs",
        counts[2]
    )

with col4:
    st.metric(
        "Employees",
        counts[3]
    )

st.divider()

# ----------------------------------
# Top Employees Chart
# ----------------------------------

st.subheader("Top Active Employees")

employees = get_top_employees()

if employees:

    employee_df = pd.DataFrame(
        employees,
        columns=[
            "Employee",
            "Total Logs"
        ]
    )

    st.bar_chart(
        employee_df.set_index(
            "Employee"
        )
    )

else:
    st.info("No employee activity found.")

st.divider()

# ----------------------------------
# Status Distribution Chart
# ----------------------------------

st.subheader("Activity Status Distribution")

status_rows = get_status_summary()

if status_rows:

    status_df = pd.DataFrame(
        status_rows,
        columns=[
            "Status",
            "Count"
        ]
    )

    st.bar_chart(
        status_df.set_index(
            "Status"
        )
    )

else:
    st.info("No activity records found.")