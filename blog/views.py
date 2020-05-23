# from django.db.models import Count, Q
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from account.models import SubAccount
from account.forms import SubAccountForm

# from .models import Post, Author, PostView
# from marketing.models import Signup
# from .forms import CommentForm, PostForm

def index(request):
    title= "Let's Code Everything."
    context = {}
    # print("Requested User",request.user)
    if request.method == "POST":
        form= SubAccountForm(request.POST)
        if form.is_valid():
            form.save()
        form= SubAccountForm()
    else:
        form= SubAccountForm()

    context= {'form':form
    #  ,'title':title
    }
    return render( request, 'index.html', context)

def signinView(request):
    context = {
        # "message":"User Created Successfully! Please Login"
        "message":''
        }
    return render(request, 'signin.html', context)

def signupView(request):
    if request.method == "POST" and request.FILES['avatar']:
        avatar =  request.FILES['avatar']
        fs = FileSystemStorage()
        filename = fs.save(avatar.name, avatar)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)

        user = User.objects.create_user(username=request.POST['username'],\
             email=request.POST['useremail'], password=request.POST['password'])
             
    context= {}

    return render(request, 'signup.html')