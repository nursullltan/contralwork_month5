from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User 

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id username'.split()

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = 'id author body created_at updated_at is_approved'.split()
        read_only_fields = 'id author body created_at updated_at is_approved'.split()

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.IntegerField(
        source='comments.count', read_only=True
    )

    class Meta:
        model = Post
        fields = 'id author title is_published comments_count created_at'.split()
        read_only_fields = 'id author created_at'.split()


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = 'id author created_at updated_at'.split()
