from tm_api.views import RegisterViewSet, TaskViewSet, StatusViewSet, LoginTokenViewSet, \
    LoginAuthViewSet, LoginTokenRefreshViewSet, LogoutAuthViewSet, LogoutTokenViewSet
from rest_framework.routers import DefaultRouter

# router = SimpleRouter()
router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('login_token', LoginTokenViewSet, basename='login_token')
router.register('refresh_login_token', LoginTokenRefreshViewSet, basename='refresh_login_token')
router.register('login_auth', LoginAuthViewSet, basename='login_auth')
router.register('logout_token', LogoutTokenViewSet, basename='logout_token')
router.register('logout_auth', LogoutAuthViewSet, basename='logout_auth')
router.register('status', StatusViewSet, basename='status')
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = router.urls
