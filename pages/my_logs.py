import streamlit as st
import pandas as pd

from db.queries import get_user_logs, delete_daily_log

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title("My Daily Logs")

rows = get_user_logs(
    st.session_state["user_id"]
)

if rows:

    df = pd.DataFrame(
        rows,
        columns=[
            "Log ID",
            "Date",
            "Service",
            "Location",
            "Status"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info("No logs found.")
selected_log = st.selectbox(
    "Select Log",
    [row[0] for row in rows]
)
delete_daily_log(
    selected_log,
    st.session_state["user_id"]
)

col1, col2 = st.columns(2)

with col1:

    if st.button("Edit Selected Log"):

        st.session_state["edit_log_id"] = selected_log

        st.switch_page("pages/edit_log.py")

with col2:

    if st.button("Delete Selected Log"):

        selected_row = None

        for row in rows:

            if row[0] == selected_log:

                selected_row = row

                break

        if selected_row[5] != "DRAFT":

            st.error(
                "Only DRAFT logs can be deleted."
            )

        else:

            delete_daily_log(selected_log, st.session_state["user_id"])

            st.success(
                "Draft deleted successfully."
            )

            st.rerun()