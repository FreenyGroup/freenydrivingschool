from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Course, Module
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from durationwidget.widgets import TimeDurationWidget

class SearchFormA(forms.Form):
    query = forms.CharField(
        label='',
        required = True,
        widget= forms.TextInput(
            attrs={
                'class':"mr-2 form-input focus:shadow-0 rounded-lg border-0 border-r border-neutrals-l02 px-6 py-6 font-body text-base text-neutrals-g03 focus:outline-none focus:ring-0 sm:w-1/2 lg:w-3/5",
				'id':'some_id',
                'placeholder': "Search our catalogue",
                }))

ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=('title',
                                              'description', ),
                                      extra=1,
                                      can_delete=True,
                                      widgets={'description': forms.Textarea(attrs={'rows': 3}),})
class AddCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['overview'].widget.attrs.update({'rows': 4})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'bg-gray-50 border border-secondary text-gray-900 text-sm rounded-lg focus:ring-primary focus:border-primary block w-full p-2.5'
        })
    courselength = forms.DurationField(widget=TimeDurationWidget(
    show_days=True, show_hours=True, show_minutes=False, show_seconds=False
), required=False)
    class Meta:
        model = Course
        fields = ['title', 'subject', 'slug', 'price', 'overview', 'image', 'languages', 'courselength']



                                      
