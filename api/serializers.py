from rest_framework import serializers
from post.models import Post

class postSerializers(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields= ['id','title','overview','created_timestamp']
    