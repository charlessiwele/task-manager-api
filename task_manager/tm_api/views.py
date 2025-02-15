from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TaskSerializer, StatusSerializer, RegisterSerializer
from rest_framework import status
from tm_api.models import Task, Status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import BasePermission
from django.contrib.auth import authenticate, login, logout


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsTaskOwner(BasePermission): 

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.user == request.user
        else:
            return False


class RegisterViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = []

        if request.user.is_authenticated:
            queryset = self.filter_queryset(self.get_queryset())

            if not request.user.is_superuser:
                queryset = queryset.filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LogoutViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer

    """
    Retrieve a model instance.
    """
    def list(self, request, *args, **kwargs):
        if request.user:
            result = logout(request)
            return Response(
                {
                    'message': 'Successful logout',
                    'status': 'success'
                }
            )
        return Response(
            {
                'message': 'No user detected to logout',
                'status': 'fail'
            }
        )


class LoginAuthViewSet(GenericViewSet, TokenObtainPairView):
    permission_classes = (AllowAny,)
    """
    Login Authentication. Creates a logged-in session on the server, alternative to generating login token.
    """
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                res = login(request, user)
                return Response(
                    {'message': 'Successful auth and login'},
                )
            else:
                return Response(
                    {
                        'message': 'invalid login credentials',
                    }, 
                )
            pass
        except Exception as err:
            return err


class LoginTokenViewSet(GenericViewSet, TokenObtainPairView):
    permission_classes = (AllowAny,)
    """
    Request a login token generation.
    """
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LoginTokenRefreshViewSet(GenericViewSet,TokenRefreshView):
    permission_classes = (AllowAny,)
    """
    Request a login token refresh.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TaskViewSet(GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            if not request.user.is_staff:
                queryset = queryset.filter(user=request.user)


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve'or  self.action == 'update':
            self.permission_classes = [IsTaskOwner, IsAdminUser] 
        return super(self.__class__, self).get_permissions()


class StatusViewSet(GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'create' or  self.action == 'update':
            self.permission_classes = [IsAdminUser] 
        return super(self.__class__, self).get_permissions()
