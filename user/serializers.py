from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import DownloadMyResume
from django.contrib.auth.models import User
from rest_framework import serializers

class ResumeSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        max_length=10000000,
        allow_empty_file=False,
        use_url=True,
        )
    class Meta:
        model = DownloadMyResume
        fields = ['file']

class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                attrs['user'] = user
                return attrs
            else:
                raise AuthenticationFailed("Invalid username or password.")
        else:
            raise serializers.ValidationError("Both username and password are required.")


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user