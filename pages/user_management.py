import streamlit as st
import pandas as pd

from db.queries import (
    get_users,
    create_user
)

if "user_id" not in st.session_state:
    st.warning("Please login first")
    st.stop()

if st.session_state["role"] != "ADMIN":
    st.error("Access Denied")
    st.stop()

st.title("User Management")

st.subheader("Add User")

employee_code = st.text_input(
    "Employee Code"
)

full_name = st.text_input(
    "Full Name"
)

role = st.selectbox(
    "Role",
    [
        "EMPLOYEE",
        "SUPERVISOR",
        "ADMIN"
    ]
)

department = st.text_input(
    "Department"
)

password = st.text_input(
    "Password"
)

if st.button("Create User"):

    create_user(
        employee_code,
        full_name,
        role,
        department,
        password,
        st.session_state["user_id"]
    )


    st.success(
        "User Created Successfully"
    )

st.subheader("Users")

rows = get_users()

df = pd.DataFrame(
    rows,
    columns=[
        "ID",
        "Employee Code",
        "Full Name",
        "Role",
        "Department",
        "Active"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)