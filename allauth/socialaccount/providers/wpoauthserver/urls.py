from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import WPOAuthServerProvider

urlpatterns = default_urlpatterns(WPOAuthServerProvider)