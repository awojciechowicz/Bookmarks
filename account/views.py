from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm)
from django.http import HttpResponse
from .models import Profile
from django.contrib import messages

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(
#                 request,
#                 username=username,
#                 password=password,
#             )
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse(
#                         "Uwierzytelnienie zakonczylo sie sukcesem."
#                     )
#                 else:
#                     return HttpResponse("Konto jest zablokowane.")
#             else:
#                 return HttpResponse("Nieprawidlowe dane logowania.")
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu urzytkownika; jednak jeszcze nie zapisujemy go
            # w bazie danych
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasla
            new_user.set_password(
                user_form.cleaned_data['password']
                )
            # Zapisanie obiektu User
            new_user.save()
            # Utworzenie profilu użytkownika
            Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Uaktualnienie profilu zakonczylo sie sukcesem'
            )
        else:
            messages.error(
                request,
                'Wystapil blad podczas aktualizacji profilu'
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )