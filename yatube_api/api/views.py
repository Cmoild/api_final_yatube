from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from .permissions import IsAuthorOrReadOnly, FollowPermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
)
from posts.models import Post, Comment, Group, Follow
from .pagination import OptionalLimitOffsetPagination
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from .authentication import (
    CustomTokenVerifySerializer, CustomTokenRefreshSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = OptionalLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, serializer):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [FollowPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
