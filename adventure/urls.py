from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('maze', api.get_maze),
    url('move', api.move),
    url('say', api.say),
]
