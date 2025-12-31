from rest_framework import serializers
from .models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ['id', 'author', 'content', 'created_at']
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        # fields = ['id', 'title', 'content', 'comments']
        fields = '__all__'