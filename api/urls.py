from django.urls import path
from .views import apiOverview, postList, postDetail, getKeywords

urlpatterns= [
    path('', apiOverview, name='api-overview'),
    path('post-list', postList, name='post-list'),
    path('post-detail/<str:pk>', postDetail, name='post-detail'),
    path('keyword-list', getKeywords, name='keyword-list'),

]