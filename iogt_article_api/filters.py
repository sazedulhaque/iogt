from home.models import Article
from django_filters import rest_framework as filters


class ArticleFilter(filters.FilterSet):
    language = filters.CharFilter(field_name='locale__language_code')
    owners_email = filters.CharFilter(field_name='owner__email')

    class Meta:
        model = Article
        fields = {'live', }
