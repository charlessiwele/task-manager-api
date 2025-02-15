from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from tm_api.views import RegisterViewSet, TaskViewSet, StatusViewSet, LoginTokenViewSet, LoginAuthViewSet, LoginTokenRefreshViewSet, LogoutViewSet
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.permissions import AllowAny
from django.urls import get_resolver
from rest_framework.routers import DefaultRouter, SimpleRouter

# router = SimpleRouter()
router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('login_token', LoginTokenViewSet, basename='login_token')
router.register('login_auth', LoginAuthViewSet, basename='login_auth')
router.register('refresh_login_token', LoginTokenRefreshViewSet, basename='refresh_login_token')
router.register('logout', LogoutViewSet, basename='logout')
router.register('status', StatusViewSet, basename='status')
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = router.urls
