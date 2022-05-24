
from django.shortcuts import render
from rest_framework import response,status,permissions
from rest_framework.generics import GenericAPIView
from Authentication.serializers import Registerserializer,LoginSerializer
from django.contrib.auth import authenticate





class AuthApiView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self,request):


        print(request)

        user = request.user
        print(user)
        serializer = Registerserializer(user)
        return response.Response({'user':serializer.data})



class RegisterApiView(GenericAPIView):


    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = Registerserializer

    def post(self,request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status = status.HTTP_200_OK)
        return response.Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class LoginApiView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    serializer_class = LoginSerializer


    def post(self,request):
        email = request.data.get('email',None)
        password = request.data.get('password',None)

        user = authenticate(username = email,password = password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data,status = status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials"},status = status.HTTP_401_UNAUTHORIZED)




