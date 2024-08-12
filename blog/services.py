from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    """
    Получение списка статей блога из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLED:
        return Blog.objects.filter(is_active=True)
    else:
        key = 'blog_list'
        articles = cache.get(key)
        if articles is not None:
            return articles
        else:
            articles = Blog.objects.filter(is_active=True)
            cache.set(key, articles)
            return articles