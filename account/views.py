from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from account.models import details
from account.serializers import UserRegistrationSerializer, UserLoginSeriaizers, UserSerializers #UserProfileSerializer,
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'User Registered Successfully'}, status=status.HTTP_201_CREATED)



class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSeriaizers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'message': 'Login Successful', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        id = user.id
        username = user.username
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        city = details.objects.get(user=user).city
        phone = details.objects.get(user=user).phone
        data = {
            "id":id,
            "username":username,
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "city":city,
            "phone":str(phone)
        }
        return Response(data,status=status.HTTP_200_OK)
        # serializer = UserProfileSerializer(request.user)
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
        user = request.user
        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Data Updated Sucesfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        try:
            user = request.user
            user.delete()
            return Response({'message':"User Deleted Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({'message':"Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
