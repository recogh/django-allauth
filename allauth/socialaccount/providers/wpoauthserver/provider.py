from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class WPOAuthServerAccount(ProviderAccount):
    def get_avatar_url(self):
        return None

    def to_str(self) -> str:
        return super(WPOAuthServerAccount, self).to_str()


class WPOAuthServerProvider(OAuth2Provider):
    id = 'wpoauthserver'
    name = 'WPOAuthServer'
    account_class = WPOAuthServerAccount

    def extract_uid(self, data) -> str:
        return data.get("uid")
    
    def extract_extra_data(self, data) -> dict:
        return data

    def extract_common_fields(self, data) -> dict:
        return dict(
                username=data.get("username"),
                first_name=data.get("first_name"),
                email=data.get("email"),
                date_joined=data.get("user_registered"))

    def get_default_scope(self) -> list:
        return ['basic']


providers.registry.register(WPOAuthServerProvider)