from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from applications.users.serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from knox.models import AuthToken



def index(request):
        return render(request,'users/index.html')

class UserRegister(generics.CreateAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

class UserLogin(generics.CreateAPIView):
	serializer_class = UserSerializer
	authentication_classes = (BasicAuthentication,)

	def post(self, request):
		token = AuthToken.objects.create(request.user)
		return Response({
			'user': self.get_serializer(request.user).data,
			'token': token
		})
