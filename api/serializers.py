from rest_framework import serializers
from .models import Post, Image, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']


class PostSerializer(serializers.ModelSerializer):
    class ImageSerializer(serializers.ModelSerializer):
        original = serializers.ImageField(read_only=True)

        class Meta:
            model = Image
            fields = ['original', 'caption']

    image = ImageSerializer()
    tag = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title', 'intro', 'slug', 'content', 'tag', 'date', 'image']
