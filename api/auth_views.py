from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response

class UserRegisterView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)

class SessionUserView(APIView):
    def get(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = UserOutSerializer(user)
        return Response(data=serializer.data)

class MyView(APIView):
    def my_view(get, request):
        output = _("Welcome to my site.")
        return Response({"message":output})
