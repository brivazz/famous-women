from django.db.models import Count
from django.core.cache import cache

from .models import Category


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_article'},
        {'title': 'Обратная связь', 'url_name': 'contact'}]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        # category = Category.objects.all()

        # читаем кэш
        category = cache.get('category')
        if not category:
            # для вывода на странице только тех категорий,
            # у которых есть хотя бы одна связанная запись:
            category = Category.objects.annotate(Count('women'))
            cache.set('category', category, 60)

        # убрать из видимости неавторизованного пользователя
        # возможность добавить новую статью:
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['categories'] = category
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context
