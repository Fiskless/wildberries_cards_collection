import datetime

from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import utc
from .models import TrackParameter


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TrackParameterForm(forms.ModelForm):

    start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local',
                                                                     'class': 'form-control'
                                                                     }
                                                              ),
                                   label='Начало отслеживания',
                                   help_text='Дата начала периода отслеживания товара',
                                   error_messages={'required': ''}
                                   )
    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local',
                                                                   'class': 'form-control'
                                                                   },
                                                              ),
                                 label='Конец отслеживания',
                                 help_text='Дата конца периода отслеживания товара',
                                 error_messages={'required': ''}
                             )

    class Meta:
        model = TrackParameter
        fields = ('article', 'start_at', 'end_at', 'time_interval')

    def clean_end_at(self):
        cd = self.cleaned_data
        if cd['end_at'] < datetime.datetime.utcnow().replace(tzinfo=utc):
            raise forms.ValidationError('End time should be more current time')
        if cd['start_at'] >= cd['end_at']:
            raise forms.ValidationError('Start time should be less end time')
        return cd['end_at']

    def clean_start_at(self):
        cd = self.cleaned_data
        if cd['start_at'] < datetime.datetime.utcnow().replace(tzinfo=utc):
            raise forms.ValidationError('Start time should be more or equal current time')
        return cd['start_at']
