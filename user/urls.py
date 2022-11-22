from django.urls import path
from . import views


urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    #path('profile/<email>', views.profile, name='profile'),
    path('userupdate/', views.UserUpdate.as_view(), name='userupdate')
]
