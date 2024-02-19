from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(max_length=20)
    fullname = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)


class ForgotPasswordSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=40)

