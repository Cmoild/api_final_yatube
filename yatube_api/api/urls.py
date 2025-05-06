from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    PostViewSet, CommentViewSet, GroupViewSet,
    FollowViewSet, CustomTokenRefreshView, CustomTokenVerifyView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/jwt/refresh/',
         CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('v1/jwt/verify/',
         CustomTokenVerifyView.as_view(), name='token_verify'),
    path('v1/jwt/create/', TokenObtainPairView.as_view(), name='token-create'),
    path('v1/posts/<int:post_pk>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='comment-list'),
    path('v1/posts/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='comment-detail'),
    path('v1/follow/', FollowViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='follow'),
    path('v1/groups/', GroupViewSet.as_view({
        'get': 'list',
    }), name='group-list'),
    path('v1/groups/<int:pk>/', GroupViewSet.as_view({
        'get': 'retrieve',
    }), name='group-detail'),
]
