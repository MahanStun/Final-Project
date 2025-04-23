from rest_framework import serializers
from .models import My_Blog

class MyBlogSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=150)
    image = serializers.ImageField(default="")
