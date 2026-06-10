import streamlit as st
import pandas as pd
if st.session_state["role"] in [
    "ADMIN",
    "SUPERVISOR"
]:
    st.page_link(
        "pages/supervisor_dashboard.py",
        label="Supervisor Dashboard"
    )
    
from db.queries import (
    get_dashboard_counts,
    get_recent_logs,
    get_log_statistics,
    update_last_login
)

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title("Dashboard")

st.write(
    f"Welcome, {st.session_state['full_name']}"
)

st.sidebar.success(
    f"Logged in as\n{st.session_state['full_name']}"
)

st.sidebar.write(
    f"Role: {st.session_state['role']}"
)

if st.sidebar.button("Logout"):

    st.session_state.clear()

    st.switch_page("app.py")

st.page_link(
    "pages/profile.py",
    label="My Profile"
)
update_last_login(
    st.session_state["user_id"]
)
st.page_link(
    "pages/change_password.py",
    label="Change Password"
)
counts = get_dashboard_counts(
    st.session_state["user_id"]
)

total_logs = counts[0] or 0
draft_logs = counts[1] or 0
submitted_logs = counts[2] or 0
approved_logs = counts[3] or 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Logs",
        total_logs
    )

with col2:
    st.metric(
        "Draft",
        draft_logs
    )

with col3:
    st.metric(
        "Submitted",
        submitted_logs
    )

with col4:
    st.metric(
        "Approved",
        approved_logs
    )

st.subheader("Recent Activities")

rows = get_recent_logs(
    st.session_state["user_id"]
)

df = pd.DataFrame(
    rows,
    columns=[
        "Log Date",
        "Service",
        "Status"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

stats = get_log_statistics(
    st.session_state["user_id"]
)

if stats:

    chart_df = pd.DataFrame(
        stats,
        columns=[
            "Status",
            "Count"
        ]
    )

    st.subheader(
        "Activity Status Summary"
    )

    st.bar_chart(
        chart_df.set_index("Status")
    )