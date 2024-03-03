"""
This module provides an authentication class, Authenticator, for handling JWT-based
authentication in Streamlit applications using API calls.
"""
from datetime import timedelta, datetime
from typing import Optional

import extra_streamlit_components as stx
import requests
import streamlit as st

from .utils import setup_session_keys


class Authenticator:
    """
        A class for handling authentication in Streamlit applications using JWT API's.

        Parameters:
        - url (str): The authentication endpoint URL.
        - method (str, optional): The HTTP method for authentication requests.
            Defaults to "post".
        - headers (dict, optional): Additional headers to include in authentication requests.
        - response_handler (callable, optional): A function to process the authentication response.
        - token_key (str, optional): The key to identify the authentication token in the response.
            Defaults to "access".
        - cookie_lifetime (timedelta, optional): The lifetime of the authentication cookie.
            Defaults to timedelta(minutes=15).
    """

    def __init__(self,
                 url: str,
                 method: str = "post",
                 headers: dict = None,
                 response_handler=None,
                 token_key: str = "access",
                 cookie_lifetime: timedelta = timedelta(minutes=15)
                 ):
        """
        Initializes the Authenticator instance with the specified parameters.
        """
        self.configuration = url
        self.method = method
        self.headers = headers
        self.response_handler = response_handler
        self.token_key = token_key
        self.cookie_lifetime = cookie_lifetime

        self.cookie_manager = stx.CookieManager()
        self.cookie_keys = []
        setup_session_keys()

    def _set_error(self, message):
        """
        Internal method to set an authentication error message.

        Parameters:
        - message (str): The error message to log.
        """

    def _check_cookie(self):
        """
        Internal method to check the authentication status based on the stored cookie.

        Returns:
        bool: True if the user is authenticated, False otherwise.
        """
        authentication_status = bool(self.cookie_manager.get(self.token_key))
        st.session_state['authentication_status'] = authentication_status
        return authentication_status

    def _cache_response(self, response):
        """
        Internal method to cache the authentication response in cookies.

        Parameters:
        - response (dict): The authentication response to cache.
        """
        for k, v in response.items():
            self.cookie_manager.set(k, v, key=k, expires_at=datetime.now() + self.cookie_lifetime)
            if k not in self.cookie_keys:
                self.cookie_keys.append(k)

    def _check_credentials(self, username, password):
        """
        Internal method to authenticate the user with provided credentials.

        Parameters:
        - username (str): The username for authentication.
        - password (str): The password for authentication.

        Returns:
        bool: True if authentication is successful, False otherwise.
        """
        if not username or not password:
            self._set_error("Please provide username and password")

        response = requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            data={"username": username, "password": password},
            timeout=5
        )
        if not response.ok:
            self._set_error(f"Response: {response.status_code}. Detail {response.text}")
            return False

        if self.response_handler:
            response = self.response_handler(response)
        else:
            response = response.json()

        self._cache_response(response)
        st.session_state['authentication_status'] = True
        return True

    def _implement_logout(self):
        """
        Internal method to implement logout functionality by clearing cookies and session state.
        """
        self.cookie_manager.delete(self.token_key)
        for k in self.cookie_keys:
            self.cookie_manager.delete(k)

        st.session_state['username'] = None
        st.session_state['authentication_status'] = None

    def login(self, location: str = 'main'):
        """
        Method to display a login form and handle authentication.

        Parameters:
        - location (str, optional): Location to display the login form, either 'main' or 'sidebar'.
            Defaults to 'main'.

        Usage:
        ```
        authenticator = Authenticator(...)
        authenticator.login()
        ```

        """
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('JWTLogin')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('JWTLogin')
                else:
                    self._set_error('Invalid location! Available locations: ["main", "sidebar"].')

                username = login_form.text_input("Username")
                password = login_form.text_input('Password', type='password')
                st.session_state['username'] = username

                if login_form.form_submit_button("Login"):
                    self._check_credentials(username, password)

    def logout(
            self,
            location: str = 'main',
            button_name: str = 'Logout',
            key: Optional[str] = None
    ):
        """
        Method to handle user logout form.

        Parameters:
        - location (str, optional): Location to display the logout button,
            either 'main' or 'sidebar'. Defaults to 'main'.
        - button_name (str, optional): The label for the logout button.
            Defaults to 'Logout'.
        - key (str, optional): A key to associate with the logout button for Streamlit.
            Defaults to None.

        Usage:
        ```
        authenticator = Authenticator(...)
        authenticator.login()

        if st.session_state["authentication_status"]:
            authenticator.logout()
        """
        if location == 'main':
            if st.button(button_name, key):
                self._implement_logout()
        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                self._implement_logout()
