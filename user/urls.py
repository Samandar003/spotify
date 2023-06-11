from django.urls import path
from .views import SignUpView, LoginViewSet, LogoutViewSet, ResumeAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("login", LoginViewSet, basename="login")
router.register("logout", LogoutViewSet, basename="logout")

urlpatterns = [
    path("singup/", SignUpView.as_view(), name='singup'),
    path('download-resume', ResumeAPIView.as_view(), name="download-my-resume")
]
urlpatterns += router.urls

