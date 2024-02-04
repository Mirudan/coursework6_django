from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('view_all/', cache_page(60)(ArticleListView.as_view()), name='blog'),
    path('view/<slug:slug>/', (ArticleDetailView.as_view()), name='view_article'),
]
