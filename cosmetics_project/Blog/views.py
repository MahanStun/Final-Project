from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from datetime import date
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
import json
from .models import *
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from .models import *
from .forms import *
from rest_framework.views import APIView
from .serializers import MyBlogSerializers,BlogModelSerializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from dashboard.models import Blog
from rest_framework import viewsets


class GetAllData(APIView):
    def get(self, request):
        query = Blog.objects.all()
        serializers = BlogModelSerializers(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class GetFavData(APIView):
    def get(self, request):
        query = Blog.objects.filter(fav=True)
        serializers = BlogModelSerializers(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class PostModelData(APIView):
    def post(self, request):
        serializers = BlogModelSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


class PostData(APIView):
    def post(self, request):
        serializers = MyBlogSerializers(data=request.data)
        if serializers.is_valid():
            title  = serializers.data.get("title")
            content = serializers.data.get("content")
            if 'image' in request.FILES:
                image = request.FILES['image']
                print(image.content_type)
            self.add_data_to_db(title, content, image)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_data_to_db(self, title , content, image):
        book = Blog()
        book.title  = title 
        book.content = content
        book.image = image
        book.save()
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, "Blog/index.html", {"blogs": blogs})
