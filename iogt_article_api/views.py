from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework import generics, mixins

from home.models import Article
from iogt_article_api.serializers import ArticleSerializer


class ArticleViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
