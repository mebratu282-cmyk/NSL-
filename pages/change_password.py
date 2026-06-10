import streamlit as st

from db.queries import (
    get_password_hash,
    change_password
)

from utils.security import (
    verify_password,
    hash_password
)

if "user_id" not in st.session_state:
    st.stop()

st.title("Change Password")

current_password = st.text_input(
    "Current Password",
    type="password"
)

new_password = st.text_input(
    "New Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)

if st.button("Change Password"):

    stored_hash = get_password_hash(
        st.session_state["user_id"]
    )

    if not verify_password(
        current_password,
        stored_hash
    ):
        st.error(
            "Current password is incorrect"
        )
        st.stop()

    if new_password != confirm_password:
        st.error(
            "Passwords do not match"
        )
        st.stop()

    if len(new_password) < 8:
        st.error(
            "Password must be at least 8 characters"
        )
        st.stop()

    hashed_password = hash_password(
        new_password
    )

    change_password(
        st.session_state["user_id"],
        hashed_password
    )

    st.success(
        "Password changed successfully"
    )