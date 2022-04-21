from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.urls import reverse
from .forms import LoginForm, UserRegistrationForm, TrackParameterForm
from .tasks import update_product_data


@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
        return redirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login', args=[0]))


@login_required
def create_product_track(request):
    if request.method == 'POST':
        form = TrackParameterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_track = form.save()
            new_track.user.add(request.user)
            res = update_product_data.delay(cd['article'])
            return redirect('/')
    else:
        form = TrackParameterForm()
    return render(request, 'track_parameters.html', {'form': form})