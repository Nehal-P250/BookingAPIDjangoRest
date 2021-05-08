from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Advisor
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
    
    

