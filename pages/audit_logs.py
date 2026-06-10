import streamlit as st
import pandas as pd

from db.queries import get_audit_logs

if "user_id" not in st.session_state:
    st.stop()

if st.session_state["role"] != "ADMIN":
    st.error("Access Denied")
    st.stop()

st.title("Audit Logs")

rows = get_audit_logs()
action_filter = st.selectbox(
    "Action Type",
    [
        "ALL",
        "LOGIN",
        "CREATE_LOG",
        "APPROVE_LOG",
        "REJECT_LOG",
        "CHANGE_PASSWORD"
    ]
)
df = pd.DataFrame(
    rows,
    columns=[
        "Date",
        "User",
        "Action",
        "Details"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)