import streamlit as st

from db.queries import (
    get_submitted_logs,
    approve_log,
    reject_log
)

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

if st.session_state["role"] != "SUPERVISOR":
    st.error("Access Denied")
    st.stop()

st.title("Supervisor Approval")

logs = get_submitted_logs()

if not logs:
    st.info("No submitted logs found")

for row in logs:

    log_id = row[0]
    employee = row[1]
    service = row[2]
    log_date = row[3]
    activity = row[4]

    st.markdown("---")

    st.write(f"Employee: {employee}")
    st.write(f"Service: {service}")
    st.write(f"Date: {log_date}")
    st.write(f"Activity: {activity}")

    comments = st.text_area(
        f"Comments_{log_id}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            f"Approve {log_id}"
        ):

            approve_log(
                log_id,
                st.session_state["user_id"],
                comments
            )

            st.success(
                "Approved Successfully"
            )

            st.rerun()

    with col2:

        if st.button(
            f"Reject {log_id}"
        ):

            reject_log(
                log_id,
                st.session_state["user_id"],
                comments
            )

            st.success(
                "Rejected Successfully"
            )

            st.rerun()