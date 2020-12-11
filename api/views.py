from rest_framework import viewsets, pagination
from rest_framework.response import Response
from collections import OrderedDict
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer

# Create your views here.

class PostPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 24

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('current', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('last_page', self.page.paginator.num_pages),
            ('results', data)
        ]))


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Post.on_site.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination


class TaggedPostViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.on_site.all()
    serializer_class = TagSerializer

    def retrieve(self, request, slug=None):
        queryset = Post.on_site.all()
        posts = get_list_or_404(queryset, tag__slug=slug)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
