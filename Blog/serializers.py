from rest_framework import serializers
from .models import My_Blog
from dashboard.models import Blog
class MyBlogSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title  = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=150)
    image = serializers.ImageField(default="")


class BlogModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"