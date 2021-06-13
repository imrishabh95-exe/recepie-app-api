from django.shortcuts import render

from rest_framework import generics

# Create your views here.
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    '''create anew user in system'''
    serializer_class = UserSerializer