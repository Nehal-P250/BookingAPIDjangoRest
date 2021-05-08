from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Advisor,MyUser
from .serializers import (MyUserSerializer,AdvisorSerializer)
# Create your views here.

class AdvisorView(APIView):
    def post(self,request,*args, **kwargs):
        print("inside the AdvisorView Post", request.data)
        serializer = AdvisorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request, *args, **kwargs):
        qs = Advisor.objects.all()
        serializer = AdvisorSerializer(qs, many=True)
        return Response(serializer.data)

class MyUserView(APIView):

    def post(self,request,*args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            retval = {'id':serializer.data["id"]}
            return Response(retval,status = status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request, *args, **kwargs):
        # qs = Advisor.objects.all()
        # serializer = AdvisorSerializer(qs, many=True)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):

    def post(self,request,*args, **kwargs):
        
        if not ('email' in request.data):
            # one or both the field/'s not preset   
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not ('password' in request.data):
            # one or both the field/'s not preset   
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data['email']
        password = request.data['password']
        
        current_user = MyUser.objects.filter(email = email).first()
        
        if current_user is None:
            # user does not exist
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.check_password(password):
            # password does not match 
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else : 
            # valid user (email, password )MATCH.
            return Response({'user_id' : current_user.id})
