from datetime import datetime  
from django.db import models
from django.contrib.auth import get_user_model
from tinymce import HTMLField
from django.template.defaultfilters import slugify
from django.urls import reverse
from account.models import Account
from django.db.models import F

User = get_user_model() 
    
# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField()
    
#     def __str__(self):
#         return self.user.username
    

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Comment(models.Model):

    username= models.CharField(max_length=20,blank=False,null=False)
    email = models.EmailField(blank=False, null=False)
    content = models.TextField()
    modified_timestamp = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey('Post',related_name='get_comments', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content

    @property
    def get_user(self):
        user =Account.objects.filter(email=self.email)
        if user:
            return user[0]
        else:
            return None
    @property
    def is_registered_comment(self):
        user =Account.objects.filter(email=self.email)
        if user:
            return True
        else:
            return False
        

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def addView(self):
        self.count= F('count')+1
        self.save()

    def __str__(self):
        return self.user.email + ' viewed ' + self.post.slug

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField('Content')
    slug = models.SlugField(unique=True)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    feature_image = models.ImageField(upload_to='posts/', blank=True, default='defaults/blog_featured.jpg')
    cover = models.ImageField(upload_to='posts/', blank=True, default='defaults/blog_cover.jpg')
    thumbnail = models.ImageField(upload_to='posts/', blank=True, default='defaults/blog_thumbnail.jpg')
    thumbnail_small = models.ImageField(upload_to='posts/', blank=True, default='defaults/blog_small_thumnnail.jpg')
    previous_post = models.ForeignKey('self'\
        ,related_name='whose_previous_post',\
        on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self'\
        ,related_name='whose_next_post',\
        on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author_posts')
    categories = models.ManyToManyField(Category)
    is_draft = models.BooleanField(default=False)
    
    @property
    def view_count(self):
        posts = PostView.objects.filter(post=self)
        count= 0
        for p in posts:
            count = p.count+ count
        return  count
    
    @property
    def comment_count(self):
        return  Comment.objects.filter(post=self).count()  

    @property
    def comments(self):
        return self.get_comments.all().order_by('modified_timestamp')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.id:
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={
            'slug':self.slug
        })

