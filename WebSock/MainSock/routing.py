from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/widget/<widget_id>/', consumers.WidgetConsumer.as_asgi()),
]