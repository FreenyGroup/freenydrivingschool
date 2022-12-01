"""educa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from courses.views import CourseListView, FeaturedCourseListView
from django.contrib.sitemaps.views import sitemap
from courses.sitemaps import CourseSitemap
from django.conf.urls import handler500, handler404


sitemaps = {
    'courses': CourseSitemap,
}
from payment import webhooks

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(),
          name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(),
          name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(),
          name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('info/', include('info.urls')),
    path('course/', include('courses.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payment/', include('payment.urls')),
    path('coupons/', include('coupons.urls')),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('', FeaturedCourseListView.as_view(), name='featured_course_list'),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += [
    path('payment/webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]

admin.site.site_header = "Freeny Driving School Admin Dashboard"
admin.site.site_title = "Freeny Driving School"
admin.site.index_title = "Welcome To Freeny Driving School's Admin Site"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)