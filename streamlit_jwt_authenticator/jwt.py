from datetime import timedelta, datetime
from typing import Optional

import extra_streamlit_components as stx
import requests
import streamlit as st

from streamlit_jwt_authenticator.utils import setup_session_keys


class Authenticator:
    def __init__(self,
                 url: str,
                 method: str = "post",
                 headers: dict = None,
                 response_handler=None,
                 token_key: str = "access",
                 cookie_lifetime: timedelta = timedelta(minutes=15)
                 ):
        self.url = url
        self.method = method
        self.headers = headers
        self.response_handler = response_handler
        self.token_key = token_key
        self.cookie_lifetime = cookie_lifetime

        self.cookie_manager = stx.CookieManager()
        self.cookie_keys = []
        setup_session_keys()

    def _set_error(self, message):
        pass

    def _check_cookie(self):
        authentication_status = bool(self.cookie_manager.get(self.token_key))
        st.session_state['authentication_status'] = authentication_status
        return authentication_status

    def _cache_response(self, response):
        for k, v in response.items():
            self.cookie_manager.set(k, v, key=k, expires_at=datetime.now() + self.cookie_lifetime)
            if k not in self.cookie_keys:
                self.cookie_keys.append(k)

    def _check_credentials(self, username, password):
        if not username or not password:
            self._set_error("Please provide username and password")

        response = requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            data={"username": username, "password": password}
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
        self.cookie_manager.delete(self.token_key)
        for k in self.cookie_keys:
            self.cookie_manager.delete(k)

        st.session_state['username'] = None
        st.session_state['authentication_status'] = None

    def login(self, location: str = 'main'):
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('JWTLogin')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('JWTLogin')
                else:
                    return self._set_error('Invalid location! Available locations: ["main", "sidebar"].')

                username = login_form.text_input("Username")
                password = login_form.text_input('Password', type='password')
                st.session_state['username'] = username

                if login_form.form_submit_button("Login"):
                    self._check_credentials(username, password)

    def logout(self, location: str = 'main', button_name: str = 'Logout', key: Optional[str] = None):
        if location == 'main':
            if st.button(button_name, key):
                self._implement_logout()
        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                self._implement_logout()
