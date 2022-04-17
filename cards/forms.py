from django.contrib.auth.models import User
from django import forms
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
                                                                     },
                                                              format='%Y-%m-%d, %H:%M'
                                                              ),
                                   label='Начало отслеживания',
                                   help_text='Дата начала периода отслеживания товара',
                                   error_messages={'required': ''}
                                   )
    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local',
                                                                     'class': 'form-control'
                                                                     },
                                                              format='%Y-%m-%d, %H:%M'
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
        if cd['start_at'] >= cd['end_at']:
            raise forms.ValidationError('Start data should be less end data')
        return cd['end_at']
