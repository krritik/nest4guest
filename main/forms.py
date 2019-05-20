from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30)
    last_name = forms.CharField(max_length = 30)
    email = forms.EmailField(max_length=200, help_text='required')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class DateInput(forms.DateInput):
    input_type = 'date'


class ReservationForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)

class GuestDetailsForm(forms.Form):
    first_name = forms.CharField(max_length = 100, required=True)
    last_name = forms.CharField(max_length = 100, required=True)
    phone = forms.IntegerField(min_value=1000000000, max_value=9999999999)
    email = forms.EmailField(required=True)                 


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feed']