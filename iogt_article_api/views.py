import django_filters.rest_framework

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions, filters
from home.models import Article
from iogt_article_api.filters import ArticleFilter
from iogt_article_api.serializers import ArticleSerializer


class ArticleViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ArticleFilter
    queryset = Article.objects.filter()
    search_fields = ['slug', 'title', 'body', 'url_path']
    ordering_fields = ['slug', 'title', 'locale', 'id', 'latest_revision_created_at', 'url_path']
    ordering = ['slug']
