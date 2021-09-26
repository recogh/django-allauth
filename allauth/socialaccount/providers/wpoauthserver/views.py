import requests

from allauth.socialaccount import app_settings

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from allauth.socialaccount.providers.oauth2.client import OAuth2Error

from .provider import WPOAuthServerProvider


class WPOAuthServerAdapter(OAuth2Adapter):
    provider_id = WPOAuthServerProvider.id

    settings = app_settings.PROVIDERS.get(provider_id)
    provider_base_url = settings.get("API_URL")

    if not provider_base_url:
        raise ValueError("Provider API URL required. Please set it in settings.py")

    access_token_url = f'{provider_base_url}/oauth/token'
    authorize_url = f'{provider_base_url}/oauth/authorize'
    identity_url = f'{provider_base_url}/oauth/me'

    supports_state = True

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_data(token.token)
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

    def get_data(self, token):
        # Verify the user first
        resp = requests.get(
            self.identity_url,
            headers={"Authorization": f"Bearer {token}"}
        )
        resp = resp.json()

        if not resp.get('ID'):
            raise OAuth2Error()

        info = dict(
            uid = resp.get("ID"),
            username=resp.get("user_login"),
            first_name=resp.get("display_name"),
            email=resp.get("user_email"),
            date_joined=resp.get("user_registered")
        )

        return info


oauth2_login = OAuth2LoginView.adapter_view(WPOAuthServerAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(WPOAuthServerAdapter)