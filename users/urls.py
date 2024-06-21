from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('profile/update_info/', ProfileViewSet.as_view({'put': 'update_info'}), name='profile-update_info'),
    path('profile/upload_photo/', ProfileViewSet.as_view({'post': 'upload_photo'}), name='profile-upload_photo'),
    path('profile/deactivate/', ProfileViewSet.as_view({'post': 'deactivate'}), name='profile-deactivate'),
    path('auth/signup/', AuthViewSet.as_view({'post': 'signup'}), name='auth-signup'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='auth-login'),
    path('auth/logout/', AuthViewSet.as_view({'post': 'logout'}), name='auth-logout'),
]
