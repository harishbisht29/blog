
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
    path('create/', postTemlatePickerView, name='post_template_picker'),
    path('create1/', postCreateView, name='post_create'),
    path('create1/<str:template_id>', postCreateView, name='post_create'),
    path('update/<slug:slug>/',postUpdateView,name='post_update'),
    path('delete/<slug:slug>/',postDeleteView,name='post_delete'),
    path('suggest/',postSuggestView,name='post_suggest'),
]
