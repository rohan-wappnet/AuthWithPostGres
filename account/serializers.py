from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import details
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UserExtraDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = details
        fields = ['city', 'phone']

class UserRegistrationSerializer(serializers.ModelSerializer):
    extra_details = UserExtraDetailsSerializer()
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=("email already exists"),
            )
        ],
    )
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name','last_name', 'extra_details']
        extra_kwarg={
            'password':{'write_only':True}
        }


        
    def create(self, validate_data):
        u = {
            "username" : validate_data['username'],
            "email" : validate_data['email'],
            "password": make_password(validate_data['password']),
            "first_name" : validate_data['first_name'],
            "last_name" : validate_data['last_name']
        }
        user = User.objects.create(**u)

        extra_detail = {
            "city" : validate_data["extra_details"]["city"],
            "phone" : validate_data["extra_details"]["phone"]
        }
        return details.objects.create(user=user, **extra_detail)
        # return User.objects.create_user(**validate_data)


class UserLoginSeriaizers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

# class UserProfileSerializer(serializers.ModelSerializer):
    # extra_details = UserExtraDetailsSerializer()
    # class Meta:
    #     model = User
    #     fields = ['id', 'username', 'email', 'first_name','last_name']

class UserSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    city = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'city']
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']

        other_details = details.objects.get(user=instance)
        other_details.city = validated_data['city']
        
        instance.save()
        other_details.save()

        # print(instance)
        return instance