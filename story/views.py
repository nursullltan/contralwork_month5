from django.shortcuts import render
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import (AuthorSerializer, CommentSerializer, 
                          PostListSerializer, PostDetailSerializer)
from .permission import IsAuthorOrReadOnly
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework import mixins, status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class UpdateDestroyAPIView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CustomPagination(PageNumberPagination):
    page_size = 5
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
    
class PostListAPIView(ListCreateAPIView):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrReadOnly]

class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthorOrReadOnly]

class CommentListAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.select_related('author').filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'id'


# Create your views here.
