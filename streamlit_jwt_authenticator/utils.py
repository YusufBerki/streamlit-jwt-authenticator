"""
Utility functions for Streamlit JWT Authenticator module.
"""
import streamlit as st


def setup_session_keys():
    """
    Sets up default session keys in Streamlit session_state.

    This function initializes default session keys, such as "username" and
    "authentication_status", in Streamlit's session_state. These keys are
    used to store and retrieve information about the user's authentication status.

    """
    keys = ["username", "authentication_status"]
    for key in keys:
        st.session_state[key] = None
