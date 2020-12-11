from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer

# Create your views here.


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Post.on_site.all()
    serializer_class = PostSerializer


class TaggedPostViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.on_site.all()
    serializer_class = TagSerializer

    def retrieve(self, request, slug=None):
        queryset = Post.on_site.all()
        posts = get_list_or_404(queryset, tag__slug=slug)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
