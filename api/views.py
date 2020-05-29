from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import postSerializers, searchKeywordsSerializers
from post.models import Post
from marketing.models import SearchKeywords

@api_view(['GET'])
def apiOverview(request):
    api_urls= {
        'List':'/post-list',
        'Deail':'/post-detail'
    }
    return Response(api_urls)

@api_view(['GET'])
def postList(request):
    posts= Post.objects.all()
    serializer= postSerializers(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postDetail(request, pk):
    post= Post.objects.get(id=pk)
    serializer= postSerializers(post, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getKeywords(request):
    keywords= SearchKeywords.objects.all()
    serializer= searchKeywordsSerializers(keywords, many=True)
    return Response(serializer.data)

