# sendemail/urls.py
from django.contrib import admin
from django.urls import path

from .views import contactView, successView, privacy

urlpatterns = [
    path("contact/", contactView, name="contact"),
    path("success/", successView, name="success"),
    path("privacy/", privacy, name="privacy"),
]