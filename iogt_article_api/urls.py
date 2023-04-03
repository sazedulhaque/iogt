from rest_framework.routers import DefaultRouter

from iogt_article_api import views

router = DefaultRouter()
router.register(r'', views.ArticleViewSet, basename='articles')
