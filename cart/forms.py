from django import forms
from courses.models import Course

COURSE_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
class CartAddCourseForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=COURSE_QUANTITY_CHOICES,
                                label=False,
                                coerce=int,
                                widget=forms.Select(attrs={'class': 'border-0 text-xs focus:outline-none focus:border-secondary focus:ring-1 focus:ring-secondary', 'style': 'background-color: transparent;'})
                                )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
