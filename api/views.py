from rest_framework import viewsets
from rest_framework.response import Response
from collections import OrderedDict
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator, EmptyPage
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


class TaggedPostViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.on_site.all()
    serializer_class = TagSerializer

    def retrieve(self, request, slug=None):
        queryset = Post.on_site.all()
        posts = get_list_or_404(queryset, tag__slug=slug)
        try:
            paginator = Paginator(posts, 12, allow_empty_first_page=False)
            page_number = int(request.GET.get('page', 1))
            page_obj = paginator.page(page_number)
            if page_obj.has_next():
                next_page_number = page_obj.next_page_number()
            else:
                next_page_number = None
            if page_obj.has_previous():
                previous_page_number = page_obj.previous_page_number()
            else:
                previous_page_number = None
            serializer = PostSerializer(page_obj, many=True)
            return Response(OrderedDict([
                ('current', page_number),
                ('next', next_page_number),
                ('previous', previous_page_number),
                ('last_page', paginator.num_pages),
                ('results', serializer.data),
            ]))
        except (EmptyPage, ValueError):
            return Response({
                "detail": "Invalid page."
            })
