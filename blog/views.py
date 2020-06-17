# from django.db.models import Count, Q
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from account.models import SubAccount
from account.forms import SubAccountForm
from post.models import Post

# from .models import Post, Author, PostView
# from marketing.models import Signup
# from .forms import CommentForm, PostForm


def getFeaturedPost():
    posts= Post.objects.filter(is_template=False)
    pview_map= [(p.id, p.view_count) for p in posts]
    pview_map.sort(key= lambda x:x[-1], reverse=True)
    if len(pview_map) < 3:
        pview_map= pview_map[len(pview_map)*-1:]
    else:
         pview_map= pview_map[-3:]

    fposts_ids= [x[0] for x in pview_map]
    fposts= posts.filter(id__in= fposts_ids )
    return fposts

def index(request):
    title= "Let's Code Everything."

    context = {}
    latest_posts= Post.objects.filter(is_template=False).order_by('-created_timestamp')[0:3] 
    featured_posts= getFeaturedPost()
    print(featured_posts)
            

    print(featured_posts)
    # print("Requested User",request.user)
    if request.method == "POST":
        form= SubAccountForm(request.POST)
        if form.is_valid():
            form.save()
        form= SubAccountForm()
    else:
        form= SubAccountForm()

    context= {'subform':form,
    'latest_posts':latest_posts,
    'featured_posts':featured_posts,
    'showGallery':True,
    'tabName':'Home'
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