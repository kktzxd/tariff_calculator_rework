from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from calculator.forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("calculator"))

    else:
        form = LoginUserForm()
    data = {'form':form}
    return render(request, 'login.html',data)
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

