from rest_framework import serializers
from post.models import Post
from marketing.models import SearchKeywords

class postSerializers(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields= ['id','title','overview','created_timestamp']
    

class searchKeywordsSerializers(serializers.ModelSerializer):
    class Meta:
        model= SearchKeywords
        fields= ['post', 'keyword','url']
    