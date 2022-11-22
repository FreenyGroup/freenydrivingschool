from django.contrib import admin
from .models import Subject, Course, Module, Language
from django.db import models
from django.forms import CheckboxSelectMultiple

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'price',
                    'available', 'created', 'updated', 'courselength']
    list_filter = ['available', 'created', 'subject',]
    list_editable = ['price', 'available',]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
