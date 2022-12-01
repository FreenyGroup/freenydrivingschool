from django.contrib import admin
from django.urls import path

from .views import contactView, successView, privacy, about

urlpatterns = [
    path("contact/", contactView, name="contact"),
    path("success/", successView, name="success"),
    path("privacy/", privacy, name="privacy"),
    path("about/", about, name="about"),
]