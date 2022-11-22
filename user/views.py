from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from .forms import UserCreationForm, UserEditForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

class StudentRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class UserUpdate(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('userupdate')

    def get_object(self):
        return self.request.user






