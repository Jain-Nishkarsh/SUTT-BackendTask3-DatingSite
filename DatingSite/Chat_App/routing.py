from django.urls import re_path
from .consumers import UserSocket

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<userID>\w+)/$", UserSocket.as_asgi()),
    # re_path(r"ws/chat/(?P<withuser>\w+)/$", ChatConsumer.as_asgi()),
    # re_path(r"ws/chat/(?P<toUser>\w+)/$", sendChannel.as_asgi()),
]