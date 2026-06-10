import streamlit as st

from datetime import date
from datetime import datetime

from db.queries import (
    get_categories,
    get_services,
    create_daily_log
)

# -----------------------------------
# Session Check
# -----------------------------------

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# -----------------------------------
# Page Title
# -----------------------------------

st.title("Daily Activity Log")

# -----------------------------------
# Date
# -----------------------------------

log_date = st.date_input(
    "Date",
    value=date.today()
)

# -----------------------------------
# Category
# -----------------------------------

categories = get_categories()

selected_category = st.selectbox(
    "Category",
    categories,
    format_func=lambda x: x[1]
)

# -----------------------------------
# Service
# -----------------------------------

services = get_services(
    selected_category[0]
)

selected_service = st.selectbox(
    "Service",
    services,
    format_func=lambda x: x[1]
)

# -----------------------------------
# Activity Description
# -----------------------------------


activity_location = st.text_input(
    "Activity Location"
)

activity_description = st.text_area(
    "Activity Description"
)

# -----------------------------------
# Start Time
# -----------------------------------

start_time = st.time_input(
    "Start Time"
)

# -----------------------------------
# End Time
# -----------------------------------

end_time = st.time_input(
    "End Time"
)

# -----------------------------------
# Outcome
# -----------------------------------

outcome = st.text_area(
    "Outcome"
)

# -----------------------------------
# Remark
# -----------------------------------

remark = st.text_area(
    "Remark"
)

# -----------------------------------
# Buttons
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button("Save Draft"):

        start_datetime = datetime.combine(
            log_date,
            start_time
        )

        end_datetime = datetime.combine(
            log_date,
            end_time
        )
        if end_datetime <= start_datetime:
            st.error("End time must be greater than start time")
            st.stop()

        duration_minutes = int(
            (end_datetime - start_datetime).total_seconds() / 60
        )

        if not activity_location:
            st.error("Please enter activity location")
            st.stop()

        if not activity_description:
            st.error("Please enter activity description")
            st.stop()

        create_daily_log(
            st.session_state["user_id"],
            log_date,
            selected_service[0],
            activity_location,
            activity_description,
            start_datetime,
            end_datetime,
            duration_minutes,
            outcome,
            remark,
            "DRAFT"
        )

        st.success("Draft Saved Successfully")


with col2:

    if st.button("Submit"):

        start_datetime = datetime.combine(
            log_date,
            start_time
        )

        end_datetime = datetime.combine(
            log_date,
            end_time
        )
        if end_datetime <= start_datetime:
            st.error("End time must be greater than start time")
            st.stop()
        duration_minutes = int(
            (end_datetime - start_datetime).total_seconds() / 60
        )
        if not activity_location:
            st.error("Please enter activity location")
            st.stop()

        if not activity_description:
            st.error("Please enter activity description")
            st.stop()



        create_daily_log(
            st.session_state["user_id"],
            log_date,
            selected_service[0],
            activity_location,
            activity_description,
            start_datetime,
            end_datetime,
            duration_minutes,
            outcome,
            remark,
            "SUBMITTED"
)

        st.success("Log Submitted Successfully")