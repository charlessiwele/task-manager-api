from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import TaskSerializer, StatusSerializer, RegisterSerializer
from rest_framework import status
from tm_api.models import Task, Status
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import BasePermission
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
import logging
logger = logging.getLogger(__name__)


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsTaskOwner(BasePermission): 
    """
    Allows access to a task to only the owner of a task
    """
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.user == request.user
        else:
            return False


class RegisterViewSet(GenericViewSet):
    """
    A viewset for handling user registration and listing users.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request):
        try:
            logger.debug('Registering user')
            serializer = self.get_serializer(data=request.data)
            is_valid = serializer.is_valid(raise_exception=True)
            if is_valid:
                serializer.save()
                logger.debug('User registered successfully')
                return Response(
                    serializer.validated_data, 
                    status=status.HTTP_200_OK
                )
        except Exception as exception:
            logger.debug('User registration failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        queryset = []

        try:
            if request.user.is_authenticated:
                logger.debug('Listing users')
                queryset = self.filter_queryset(self.get_queryset())

                if not request.user.is_superuser:
                    queryset = queryset.filter(id=request.user.pk)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            logger.debug('Users listed successfully')
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            logger.debug('Listing users failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated] 
        return super(self.__class__, self).get_permissions()



class LogoutAuthViewSet(GenericViewSet):
    """
    A viewset for handling user auth session logouts
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer
    def list(self, request, *args, **kwargs):
        try:
            logger.debug('Logging out user')
            if request.user:
                logout(request)
                logger.debug('User logged out successfully')
                return Response(
                    {
                        'message': 'Successful logout',
                        'status': 'success'
                    },
                    status=status.HTTP_200_OK
                )
            logger.debug('No user detected to logout')
            return Response(
                {
                    'message': 'No user detected to logout',
                    'status': 'fail'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as exception:
            logger.debug('User logout failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutTokenViewSet(GenericViewSet, TokenRefreshView):
    """
    A viewset for handling user token  blasklisting
    """
    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        try:
            if request.user:
                refresh_token = request.data.get("refresh")
                if not refresh_token:
                    return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the token
                logger.debug('User token blacklisted successfully')

                return Response(
                    {
                        'message': 'Successful logout',
                        'status': 'success'
                    },
                    status=status.HTTP_200_OK
                )
            logger.debug('No user detected to logout')
            return Response(
                {
                    'message': 'No user detected to logout',
                    'status': 'fail'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
        except Exception as exception:
            return Response(
                str(exception),
                status=status.HTTP_401_UNAUTHORIZED
            )



class LoginAuthViewSet(GenericViewSet, TokenObtainPairView):
    """
    Login Authentication. Creates a logged-in session on the server, alternative to generating login token.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
        try:
            logger.debug('Authenticating user')
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user:
                login(request, user)
                logger.debug('User authenticated successfully')
                return Response(
                    {
                        'session':request.session,
                        'message': 'Successful auth and login',
                    },
                    status=status.HTTP_200_OK
                )
            else:
                logger.debug('Invalid login credentials')
                return Response(
                    {
                        'message': 'invalid login credentials',
                    },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as exception:
            logger.debug('User authentication failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginTokenViewSet(GenericViewSet, TokenObtainPairView):
    """
    Token Login. Creates a login token pair (access key, refresh key).
    """
    permission_classes = (AllowAny,)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            logger.debug('Generating login token')
            serializer.is_valid(raise_exception=True)
            logger.debug('Login token generated successfully')
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as exception:
            logger.debug('Login token generation failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginTokenRefreshViewSet(GenericViewSet,TokenRefreshView):
    """
    Request a login token refresh.
    """
    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            logger.debug('Refreshing login token')
            serializer.is_valid(raise_exception=True)
            logger.debug('Login token refreshed successfully')
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as exception:
            logger.debug('Login token refresh failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskViewSet(GenericViewSet):
    """
    API endpoint that allows users to handle tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def retrieve(self, request, *args, **kwargs):
        try:
            logger.debug('Retrieving task')
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logger.debug('Task retrieved successfully')
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            logger.debug('Task retrieval failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        try:
            logger.debug('Listing tasks')
            queryset = self.filter_queryset(self.get_queryset())
            if not request.user.is_superuser:
                if not request.user.is_staff:
                    queryset = queryset.filter(user=request.user)


            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            page = self.paginate_queryset(queryset)

            serializer = self.get_serializer(queryset, many=True)
            logger.debug('Tasks listed successfully')
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            logger.debug('Task listing failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            logger.debug('Creating task')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(request)
            logger.debug('Task created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            logger.debug('Task creation failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            logger.debug('Updating task')
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug('Task updated successfully')
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def get_permissions(self):
        if self.action == 'retrieve'or  self.action == 'update':
            self.permission_classes = [IsTaskOwner, IsAdminUser, IsSuperUser] 
        else:
            self.permission_classes = [IsAuthenticated]
        return super(self.__class__, self).get_permissions()


class StatusViewSet(GenericViewSet):
    """
    API endpoint that allows statuses to be viewed or edited.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            logger.debug('Retrieving status')
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logger.debug('Status retrieved successfully')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            logger.debug('Status retrieval failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        try:
            logger.debug('Listing statuses')
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            logger.debug('Statuses listed successfully')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            logger.debug('Status listing failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            logger.debug('Creating status')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug('Status created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            logger.debug('Status creation failed ' + exception.__str__())
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            logger.debug('Updating status')
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug('Status updated successfully')

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            logger.debug('Status updated successfully')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(
                str(exception),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_permissions(self):
        if self.action == 'create' or  self.action == 'update':
            self.permission_classes = [IsSuperUser] 
        else:
            self.permission_classes = [IsAuthenticated] 
        return super(self.__class__, self).get_permissions()
