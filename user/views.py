from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm, UserEditForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

class StudentRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('userupdate')
    form_class=UserEditForm

    def get_initial(self):
        initial = super(UserProfileUpdateView, self).get_initial()
        return initial
    
    def form_valid(self, form):
        form.instance = self.request.user
        return super(UserProfileUpdateView, self).form_valid(form)
    
    def get_object(self):
        return self.request.user

class UserUpdate(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('userupdate')

    def get_object(self):
        return self.request.user






