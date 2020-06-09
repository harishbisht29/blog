
from django.urls import path, include
from .views import (
    postDetailView,
    postListView,
    postCreateView,
    postUpdateView,
    postDeleteView,
    postSuggestView,
    postTemlatePickerView,
    )
urlpatterns = [
    path('post_detail/<slug:slug>/',postDetailView,name='post_detail'),
    path('post_list/',postListView,name='post_list'),
    # 3 create urls -
    # create -  Takes to template picker
    # create_new - Creates a new article without using any template
    # create- creates a new article with the help of template
    
    path('create/', postTemlatePickerView, name='post_template_picker'),
    path('create_new/', postCreateView, name='post_create'),
    path('create_new/<str:template_id>', postCreateView, name='post_create'),
    
    path('update/<slug:slug>/',postUpdateView,name='post_update'),
    path('delete/<slug:slug>/',postDeleteView,name='post_delete'),
    path('suggest/',postSuggestView,name='post_suggest'),
]
