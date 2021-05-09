from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import datetime


import jwt, datetime

from .models import Advisor,MyUser,Booking
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
            # Email Field is not present   
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not ('password' in request.data):
            # password Field is not present    
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

        
        payload = {
            'id': current_user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        response = Response()
        token = jwt.encode(payload, 'secret', algorithm='HS256') 
        retval = {
            'user_id' : current_user.id,
            'jwt' : token
        }
        response.set_cookie(key='jwt', value=token,httponly=True)
        response.data = retval
        response.status = status.HTTP_200_OK
        
       
        
        # valid user (email, password )MATCH.
        # return Response(retval,status = status.HTTP_200_OK)
        return response



# Assumption : only allowing loged in user to view the Advisor list.
# For this jwt cookie is used for user authentication.
class GetAdvisorView(APIView):
    
    def get(self, request, userID):
        # get 
        token = request.COOKIES.get('jwt')
        print(userID)
        # return Response(token)

        # user is not loged in.
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

         
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # jwt decode failed , JWT token is not correct
            raise AuthenticationFailed('Unauthenticated!')
        
        # the url userID and payload userID does not match
        if userID != payload['id']:
            raise AuthenticationFailed('Unauthenticated!')


        qs = Advisor.objects.all()
        serializer = AdvisorSerializer(qs, many=True)
        return Response(serializer.data)
            

# Assumption : only allowing loged in user to view the Advisor list.
# For this jwt cookie is used for user authentication.
class BookAdvisorView(APIView):
    
    def get(self, request, userID, advisorID):
        # get JWT token which is set as cookie.
        token = request.COOKIES.get('jwt')
        print(userID)
        
        # user is not loged in.
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

         
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # jwt decode failed , JWT token is not correct
            raise AuthenticationFailed('Unauthenticated!')
        
        # the url userID and payload userID does not match
        if userID != payload['id']:
            raise AuthenticationFailed('Unauthenticated!')
        user = MyUser.objects.filter(id=userID).first()

        advisor = Advisor.objects.filter(id=advisorID).first()
        # no such advisor exists
        if not advisor: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not 'booking_time' in request.data:
            return Response({"Please provide booking_time in the format %d-%m-%Y %H:%M:%S"},
                            status=status.HTTP_400_BAD_REQUEST)

        # date time format
        # "%d-%m-%Y %H:%M:%S"
        time_string = request.data['booking_time']
        booking = Booking(time= datetime.datetime.strptime(time_string, "%d-%m-%Y %H:%M:%S"),user=user,advisor=advisor)
        booking.save()

        return Response(status = status.HTTP_200_OK)    