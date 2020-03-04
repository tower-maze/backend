from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """CSRF checks are great and all, but only really applicable
    for blocking attacks when either:

    1. You are using the same origin for your request and website
    2. You do not have CORS blocking request from unknown host

    Since we are using django as web server with proper CORS settings
    these types of attacks are not applicable for us and make setting
    up CSRF a hassle on the frontend since we need to provide a CSRF
    token on every request which is next to impossible to get because
    the cookie is set on a different domain.

    See: https://stackoverflow.com/questions/11008469/are-json-web-services-vulnerable-to-csrf-attacks/11024387#11024387"""

    def enforce_csrf(self, request):
        return
