from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import random
from .models import OTP
from Ai_Django.email_sending import send_otp_email



from Ai_Django.serializers import (
      SignUpSerializer,
      ForgotPasswordSerializer,

)


def signup(request):
    return render(request, "Ai_Django/signup.html")

def forgot(request):
    return render(request, "Ai_Django/forgot.html")


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            confirm_password = serializer.validated_data["confirm_password"]
            email = serializer.validated_data["email"]
            fullname = serializer.validated_data.get("fullname", "")

            if not username or not password:
                return Response(
                    {"error": "Username and password are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if password != confirm_password:
                return Response(
                    {"error": "Password is not Match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=fullname,
                )
                # Mark the user as active (verified) upon signup
                user.is_active = True
                user.save()

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response(
                    {"access_token": access_token, "refresh_token": refresh_token, "username":fullname},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data["email_or_username"]
            try:
                # Check if the provided value is an email
                if "@" in username_or_email:
                    user = User.objects.get(email=username_or_email)
                else:
                    # If not an email, assume it's a username and retrieve the email from the User model
                    user = User.objects.get(username=username_or_email)

                otp_code = str(random.randint(100000, 999999))
                print(otp_code)

                otp, created = OTP.objects.get_or_create(user=user)
                
                otp.otp = otp_code
                otp.save()
                send_otp_email(username_or_email, otp_code)

                # You can send the OTP code to the user's email here (see Step 3)

                return Response(
                    {
                        "message": "OTP has been generated and saved successfully.",
                        # "otp": otp.otp,
                    },
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
