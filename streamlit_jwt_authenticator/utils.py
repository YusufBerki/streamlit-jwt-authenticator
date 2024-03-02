import streamlit as st


def setup_session_keys():
    keys = ["username", "authentication_status", "logout"]
    for key in keys:
        st.session_state[key] = None
