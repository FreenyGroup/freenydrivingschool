from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(admin.ModelAdmin):
    exclude = ['password']
    ordering = ('email',)
    list_display = ('first_name','last_name','email','dob','nickname', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser',)
    readonly_fields = ('email',)

admin.site.register(User, CustomUserAdmin)