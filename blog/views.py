from django.views.generic import ListView, DetailView

from blog.models import Article


class ArticleListView(ListView):
    """Представление для просмотра статей блога"""
    paginate_by = 6
    model = Article
    extra_context = {'title': 'Наш бложичек'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('-created_on')
        return queryset


class ArticleDetailView(DetailView):
    """Представление для просмотра отдельной статьи"""
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj
