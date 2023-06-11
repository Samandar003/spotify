from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSignInSerializer, UserSignUpSerializer, ResumeSerializer
# Create your views here.
from django.contrib.auth import logout
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from .authentication import CsrfExemptSessionAuthentication
from .models import DownloadMyResume
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse

class ResumeAPIView(APIView):
    def get(self, request):
        obj = DownloadMyResume.objects.all().first()
        file = obj.file
        return FileResponse(file, as_attachment=True, filename=file.name)

class LoginViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # perform further actions with authenticated user
        return Response("Logged in")
    
class LogoutViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication, ]

    def create(self, request):
        logout(request)
        return Response("Logged out")
    
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # perform further actions with the created user
        return Response("User Singed up")


