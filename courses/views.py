import imp
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count, Q
from django.core.cache import cache
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from students.forms import CourseEnrollForm
from .forms import AddCourseForm, ModuleFormSet, SearchFormA
from .models import Course, Language
from .models import Module, Content
from .models import Subject
from cart.forms import CartAddCourseForm
from django.contrib.postgres.search import SearchVector, \
                                           SearchQuery, SearchRank
from durationwidget.widgets import TimeDurationWidget
from django.contrib.auth import get_user_model
User = get_user_model()

def error_404_view(request, exception):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'courses/404/404.html')

class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['title', 'subject', 'slug', 'price', 'overview', 'image', 'available', 'courselength', 'languages']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ListAndCreateView(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Course
    permission_required = ('courses.add_course','courses.view_course')
    template_name = 'courses/manage/course/list.html'
    success_url = reverse_lazy('manage_course_list')
    form_class = AddCourseForm    
    error_message = 'Error saving the Doc, check fields below.'

    #def get_form(self, form_class=None):
        #form = self.get_form_class()(**self.get_form_kwargs())
        #form.fields['overview'].widget.attrs.update({'rows': 4})
        #for field in form.fields:
            #form.fields[field].widget.attrs.update({'class':'bg-gray-50 border border-secondary text-gray-900 text-sm rounded-lg focus:ring-primary focus:border-primary block w-full p-2.5'
        #})
        #form.fields['courselength'].widget = forms.DurationField(widget=TimeDurationWidget())
        #return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["object_list"] = self.model.objects.filter(owner=self.request.user)
        return context

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    def get_form(self, form_class=None):
        form = self.get_form_class()(**self.get_form_kwargs())
        form.fields['available'].widget.attrs.update({'class':'w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'})
        form.fields['title'].widget.attrs.update({'class':'shadow-lg-sm border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-2 focus:ring-fuchsia-50 focus:border-fuchsia-300 block w-full p-2.5'
        })
        form.fields['subject'].widget.attrs.update({'class':'shadow-lg-sm border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-2 focus:ring-fuchsia-50 focus:border-fuchsia-300 block w-full p-2.5'
        })
        form.fields['price'].widget.attrs.update({'class':'shadow-lg-sm border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-2 focus:ring-fuchsia-50 focus:border-fuchsia-300 block w-full p-2.5'
        })
        form.fields['slug'].widget.attrs.update({'class':'shadow-lg-sm border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-2 focus:ring-fuchsia-50 focus:border-fuchsia-300 block w-full p-2.5'
        })
        form.fields['courselength']= forms.DurationField(widget=TimeDurationWidget(
            show_days=True, show_hours=True, show_minutes=False, show_seconds=False
        ), required=False)
        form.fields['courselength'].widget.attrs.update({'class':'shadow-lg-sm border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-2 focus:ring-fuchsia-50 focus:border-fuchsia-300 block w-full p-2.5'
        })
        form.fields['overview'].widget.attrs.update({'class':'shadow-lg-sm border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-2 focus:ring-fuchsia-50 focus:border-fuchsia-300 block w-full p-2.5'
        })
        form.fields['languages'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Language.objects.all())

        return form
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)
        
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                                data=data)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file', 'textwithimage']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                       id=module_id,
                                       course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                               id=id,
                               module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                   course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__course__owner=request.user) \
                       .update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects: 
            subjects = Subject.objects.filter(courses__available=True).annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.filter(available=True).order_by('updated').annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})

class FeaturedCourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/featured.html'
    def get(self, request, featuredsubject=None):
        featuredsubjects = cache.get('featured_subjects')
        if not featuredsubjects: 
            featuredsubjects = Subject.objects.filter(courses__available=True).order_by('courses__-updated')[:4].annotate(total_courses=Count('courses'))
            cache.set('featured_subjects', featuredsubjects)
        featured_courses = Course.objects.filter(available=True).order_by('-updated')[:5].annotate(total_modules=Count('modules'))
        if featuredsubject:
            featuredsubject = get_object_or_404(Subject, slug=featuredsubject)
            featuredkey = f'subject_{featuredsubject.id}_courses'
            featuredcourses = cache.get(featuredkey)
            if not featuredcourses:
                featuredcourses = featured_courses.filter(subject=featuredsubject)
                cache.set(featuredkey, featuredcourses)
        else:
            featuredcourses = cache.get('featured_courses')
            if not featuredcourses:
                featuredcourses = featured_courses
                cache.set('featured_courses', featuredcourses)
        return self.render_to_response({'subjects': featuredsubjects,
                                        'subject': featuredsubject,
                                        'courses': featuredcourses,})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_course_form'] = CartAddCourseForm()
        context['enroll_form'] = CourseEnrollForm(
                                   initial={'course':self.object})
        return context


def post_search(request):
    form = SearchFormA()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchFormA(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('overview', weight='B')
            search_query = SearchQuery(query)
            results = Course.objects.filter(available=True).annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

    return render(request,
                  'courses/search/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

class EnrolledStudentsListView(LoginRequiredMixin, ListView):
    model = User
    queryset = model.objects.all()
    context_object_name = 'users'
    template_name = 'courses/manage/course/students.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs.get('course', None))
        return context
    def get_queryset(self):
        queryset = super(EnrolledStudentsListView, self).get_queryset()
        course = self.kwargs.get('course', None)
        if course:
            return queryset.filter(courses_joined=course)
        return queryset
