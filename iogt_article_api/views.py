import django_filters.rest_framework

from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework import mixins
from home.models import Article
from iogt_article_api.filters import ArticleFilter, SectionFilter
from iogt_article_api.serializers import ArticleSerializer, SectionSerializer


class ArticleViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ArticleSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ArticleFilter
    queryset = Article.objects.filter()


class SectionViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SectionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = SectionFilter
    queryset = SectionSerializer.Meta.model.objects.filter()
