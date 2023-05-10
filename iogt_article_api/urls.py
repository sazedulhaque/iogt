from rest_framework.routers import DefaultRouter

from iogt_article_api import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='articles')
router.register(r'sections', views.SectionViewSet, basename='sections')
