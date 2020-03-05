from django.urls import include, path
from django.conf.urls import url
from . import api

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('authenticated/', api.logged_in),
    path('registration/', include('rest_auth.registration.urls')),
]
