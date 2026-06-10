import streamlit as st

from db.queries import (
    get_log_by_id,
    update_daily_log,
    get_approval_comments
)

if "edit_log_id" not in st.session_state:
    st.error("No log selected")
    st.stop()

log_id = st.session_state["edit_log_id"]

log = get_log_by_id(log_id)

if log is None:
    st.error(f"Log ID {log_id} not found")
    st.stop()


st.write("Session Log ID =", st.session_state.get("edit_log_id"))


log_id = st.session_state["edit_log_id"]

st.write("Log ID =", log_id)

log = get_log_by_id(log_id)

st.write("Database Result =", log)





if log[10] not in ["DRAFT", "REJECTED"]:

    st.error(
        "Only DRAFT or REJECTED logs can be edited."
    )

    st.stop()

activity_location = st.text_input(
    "Location",
    value=log[3]
)

activity_description = st.text_area(
    "Description",
    value=log[4]
)

outcome = st.text_area(
    "Outcome",
    value=log[8]
)

remark = st.text_area(
    "Remark",
    value=log[9]
)
if st.button("Save Changes"):

    update_daily_log(
        log_id,
        log[2],
        activity_location,
        activity_description,
        log[5],
        log[6],
        log[7],
        outcome,
        remark
    )

    st.success("Log Updated Successfully")


approval = get_approval_comments(log_id)

if approval:

    st.subheader("Supervisor Review")

    st.write(
        f"Status: {approval[0]}"
    )

    st.info(
        approval[1]
    )