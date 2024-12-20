from django.urls import path, include
from . import views

urlpatterns = [
    path("account_settings", views.settings, name="account_settings"),
    path("information", views.information, name="information"),
    path("security_settings", views.security_settings, name="security_settings"),
    path("", views.settings, name="settings"),
    path("account", views.settings, name="account_settings"),
    path("security", views.security_settings, name="security_settings"),
    path("notification", views.notification_settings, name="notification_settings"),
    path("chat", views.chat_settings, name="chat_settings"),
    path("toggle_2fa/", views.toggle_2fa, name="toggle_2fa"),
    path("toggle_notification_when_profile_visited", views.toggle_notification_when_profile_visited,name = "toggle_notification_when_profile_visited"),
    path("toggle_notification_to_email",views.toggle_notification_to_email,name = "toggle_notification_to_email"),
    path("set_periodicity_of_notification_reports",views.change_periodicity_of_notifications_reports,name="set_periodicity_of_notification_reports")
]
