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
from .serializers import MyBlogSerializers
from rest_framework.response import Response
from rest_framework import status



class GetAllData(APIView):
    def get(self, request):
        query = My_Blog.objects.all()
        serializers = MyBlogSerializers(query, many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

    
class PostModelData(APIView):
    def post(self, request):
        serializers = MyBlogSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


class PostData(APIView):
    def post(self, request):
        serializers = MyBlogSerializers(data=request.data)
        if serializers.is_valid():
            name = serializers.data.get("name")
            description = serializers.data.get("description")
            image = request.FILES["image"]
            self.add_data_to_db(name, description, image)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_data_to_db(self, name, description, image, fav):
        book = My_Blog()
        book.name = name
        book.description = description
        book.image = image
        book.save()
def index_Blog(request):
    My_Blogs = My_Blog.objects.all()
    return render(request, "Blog/index.html", {"My_Blogs": My_Blogs})
    #return HttpResponse("welcome")
