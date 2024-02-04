from django.db.models import Count
from django.shortcuts import render

from blog.models import Article
from clients.models import Client
from mailing.models import MailingSettings
from main.utils import cache_for_queryset


def index(request):
    """Представление для отображения главной страницы"""
    title = 'Главная страница'
    articles = Article.objects.order_by('?')[:3]
    total_mailings = MailingSettings.objects.count()
    total_active_mailings = cache_for_queryset(
        key='total_active_mailings',
        queryset=(MailingSettings.objects.
                  filter(mailing_status=MailingSettings.STATUS.RUNNING).count())
    )
    total_unique_emails = Client.objects.values('email').annotate(total=Count('email')).count()

    context = {
        'title': title,
        'blog': articles,
        'total_mailings': total_mailings,
        'total_active_mailings': total_active_mailings,
        'total_unique_emails': total_unique_emails
    }

    return render(request, 'main/index.html', context)
