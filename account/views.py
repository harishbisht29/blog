from django.shortcuts import render
from .forms import SignupForm, SigninForm
from .models import Account
# from django import forms
from django.contrib.auth import login,authenticate, logout

def signupView(request):
    form = None
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    context = {
        'form':form}
    return render(request, 'templates/signup.html',context)

def signinView(request):
    
    if request.method== "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            password= form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                context = { 'form': form, 'username': request.user.username } 
                return render(request, 'index.html',context)
            else:
                context = { 'form': form } 
                return render(request, 'templates/signin.html',context)
            
    else:
        form = SigninForm()
        context = { 'form': form } 
        return render(request, 'templates/signin.html',context)


def signoutView(request):
    if request.method == "GET":
        logout(request)
    return render(request,'index.html')