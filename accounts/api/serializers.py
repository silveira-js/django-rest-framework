import datetime
from django.contrib.auth import get_user_model
from requests.api import request
from rest_framework import serializers
from django.utils import timezone
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse


from accounts.api.utils import jwt_response_payload_handler

jwt_payload_handler            = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler             = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler   = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta                   = api_settings.JWT_REFRESH_EXPIRATION_DELTA


User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    uri         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri'
        ]
    
    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-user:detail', kwargs={'username':obj.username}, request=request)

class UserRegisterSerializer(serializers.ModelSerializer):
    # password        = serializers.CharField(style={'input_type':'password'}, write_only = True)
    password2              = serializers.CharField(style={'input_type':'password'}, write_only = True)
    token                  = serializers.SerializerMethodField(read_only=True)
    expires                = serializers.SerializerMethodField(read_only=True)
    message                = serializers.SerializerMethodField(read_only=True)
    # token_response         = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message'
            # 'token_response'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # def get_token_response(self, obj):
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     context = self.context
    #     request = context['request']
    #     print(request.user.is_authenticated )
    #     response = jwt_response_payload_handler(token, user, request=context['request'])
    #     return response

    def get_message(self, obj):
        return "Thank you for registering. Please, verify your email before continuing."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value
    
    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists")
        return value
        
    def get_token(self, obj):  #instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw   = data.get('password')
        pw2  = data.get('password2')
        if pw != pw2:
            raise serializers.ValidationError('Passowwords must match.')
        return data

    def create(self, validated_data):
        print(validated_data)
        user_obj = User(username = validated_data.get('username'),email = validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False
        user_obj.save()
        return user_obj