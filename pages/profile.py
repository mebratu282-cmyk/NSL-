import streamlit as st
import pandas as pd

from db.queries import get_user_profile, get_login_history

if "user_id" not in st.session_state:
    st.stop()

st.title("My Profile")

profile = get_user_profile(
    st.session_state["user_id"]
)

st.subheader("User Information")


st.write(f"**Employee Code:** {profile[0]}")
st.write(f"**Full Name:** {profile[1]}")
st.write(f"**Role:** {profile[2]}")
st.write(f"**Department:** {profile[3]}")
st.write(f"**Phone:** {profile[7]}")
st.write(f"**Created At:** {profile[5]}")
st.write(f"**Last Login:** {profile[6]}")




st.divider()

st.subheader("Login History")

history = get_login_history(
    st.session_state["user_id"]
)

if history:

    df = pd.DataFrame(
        history,
        columns=[
            "Login Time",
            "Details"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )