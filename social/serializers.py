from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type':"password"}
    )

    class Meta(object):
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'password', 'mobile_number', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user_model=get_user_model()
        password=validated_data.pop('password')
        user=user_model.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(
        style={'input_type':"password"},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        user=authenticate(
            username=attrs.get('username'),
            password=attrs.get('password'),
        )
        if not user:
            msg=('Unable to authenticate the user with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        
        attrs['user']=user
        return attrs