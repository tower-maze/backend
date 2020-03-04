from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('others', api.other_players),
    url('move', api.move),
    url('say', api.say),

]
