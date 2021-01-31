
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    author = serializers.CharField()
    title = serializers.CharField()
    date_posted = serializers.DateTimeField()
    thumbnail = serializers.ImageField()

    def get_image(self, obj):
        try:
            image = obj.author.profile.profile_image.url
            return image
        except ValueError:
            return None



