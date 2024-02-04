from django.core.cache import cache
from django.db.models import QuerySet

from config import settings


def cache_for_queryset(key: str, queryset: QuerySet, time: int = settings.CACHE_TIMEOUT) -> QuerySet:
    """ Кеширует запрос к базе данных """
    if not settings.CACHE_ENABLED:
        return queryset
    queryset_cache = cache.get(key)
    if queryset_cache is not None:
        return queryset_cache
    cache.set(key, queryset, time)
    return queryset
