from django.urls import path

from . import views


urlpatterns = [
    path('messages/', views.get_messages, name='get_messages'), # This path can also take the following query parameters: qstring
    path('messages/unread/', views.get_unread_messages, name='get_unread_messages'),
    path('messages/sent/', views.get_send_messages, name='get_send_messages'),
    path('messages/received/', views.get_received_messages, name='get_received_messages'),
    path('messages/<int:message_id>/', views.get_message, name='get_message'),
]