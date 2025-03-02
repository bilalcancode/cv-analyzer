from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_cv, name="upload_cv"),
    path("summary/", views.cv_summary, name="cv_summary"),
    path("upload/success/", views.upload_success, name="cv_upload_success"),
    path("chat/", views.chatbot_view, name="chatbot"),
    path("chat/clear/", views.clear_chat, name="clear_chat"),
]
