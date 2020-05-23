from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post,PostView, Comment
from account.models import Account
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm



# from marketing.models import Signup

def get_author(user):
    qs= Account.objects.filter(email=user)
    if qs.exists():
        return qs[0] 
    return None

def get_category_count():
    queryset = Post \
        .objects.filter(is_draft=False) \
        .values('categories__title') \
        .annotate(Count('categories__title'))

    return queryset

def postDetailView(request, slug):
    
    post = get_object_or_404(Post,slug=slug)
    latest_posts = Post.objects.filter(is_draft=False).order_by('-created_timestamp')[0:3] 
    category_count = get_category_count() 
    
    
    if request.user.is_authenticated:
        form = CommentForm({"username":request.user.username, "email":request.user.email })
        form.fields['username'].widget.attrs['readonly'] = "readonly"
        form.fields['email'].widget.attrs['readonly'] = "readonly"
        user = request.user
    else:
        form = CommentForm()
        user = User.objects.get(username="anonymous")
    
    p= PostView.objects.filter(user= user)
    if p:
        if not request.user.is_authenticated :
            p[0].addView()
    else:
        PostView.objects.create(user=user, post=post, count=1)
    

    print("Printing Comment Object")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.post = post
            form.save()
            return redirect(reverse("post_detail", kwargs={'slug':slug}))
    
    context = {
        'category_count':category_count,
        'latest_posts':latest_posts,
        'post':post,
        'form':form
    }
    return render(request, 'templates/post.html',context)

def postListView(request):
    search_text = request.GET.get('search_text')

    if search_text:
        all_posts = Post.objects.all()
        post_list = all_posts.filter(Q(title__icontains=search_text) \
            | Q(overview__icontains=search_text)).distinct()
        context = {
        'post_list': post_list
        }
    else:
        all_posts = Post.objects.filter(is_draft=False).    order_by('-created_timestamp')
        context = {
            'post_list':all_posts
            }
    
    paginator = Paginator(context['post_list'], 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_list = paginator.page(page)
    except PageNotAnInteger:
        paginated_list = paginator.page(1)
    except EmptyPage:
        paginated_list = paginator.page(paginator.num_pages)

    # Getting Top 3 Latest Post
    latest_posts = Post.objects.filter(is_draft=False).order_by('-created_timestamp')[0:3] 

    # Getting Category Count 
    category_count = get_category_count() 

    context = {
        'category_count': category_count,
        'latest_posts':latest_posts,
        'post_list': paginated_list,
        'page_request_var':page_request_var,
        'search_text':search_text
        
    }
    return render(request,'templates/post_list.html', context)

def postCreateView(request):
    title='Create'
    form= PostForm(request.POST or None , request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = get_author(request.user)
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'form':form,
        'page_type':title
    }
    return render(request, 'templates/post_create.html',context)

def postUpdateView(request, slug):
    # Fetch Post From Model
    post= get_object_or_404(Post, slug=slug)
    page_type = 'Update'
    form= PostForm(
        request.POST or None , 
        request.FILES or None, 
        instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = get_author(request.user)
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'form':form,
        'page_type':page_type
    }
    return render(request, 'templates/post_create.html',context)


def postDeleteView(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect(reverse("post_list"))
    
def postSuggestView(request):
    context = {}
    return render(request, 'templates/post_suggest.html',context)