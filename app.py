import streamlit as st
from db.queries import (
    authenticate_user,
    create_audit_log
)
from db.connection import get_connection

st.set_page_config(
    page_title="NSL Daily Activity Log System",
    layout="wide"
)

st.title("NSL Daily Activity Log System")

employee_code = st.text_input("Employee Code")
password = st.text_input("Password", type="password")


if st.button("Login"):

    user = authenticate_user(
        employee_code,
        password
    )

    if user:

        st.session_state["user_id"] = user[0]
        st.session_state["full_name"] = user[1]
        st.session_state["role"] = user[2]
        create_audit_log(
            user[0],
            "LOGIN",
            "User logged into the system"
        )
        st.success(f"Welcome {user[1]}")

        st.switch_page("pages/dashboard.py")

    else:
        st.error("Invalid Employee Code or Password")

