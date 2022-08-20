# from django import template
# from women.models import Category


# В начало базового шаблона добавить:
# {% load women_tags %}
# в коде добавить:
# {% main_menu as menu %} для меню и:
# либо {% show_categories '-name' category_selected %}
# либо:
# {% show_categories category_selected=category_selected %} для категорий


# register = template.Library()


# @register.simple_tag(name='categories_simple_tag')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)


# @register.inclusion_tag('tags/list_categories.html')
# def show_categories(sort=None, category_selected=0):
#     if not sort:
#         category = Category.objects.all()
#     else:
#         category = Category.objects.order_by(sort)

#     return {'categories': category, 'category_selected': category_selected}


# @register.simple_tag()
# def main_menu():
#     menu = [{'title': 'О сайте', 'url_name': 'about'},
#             {'title': 'Добавить статью', 'url_name': 'add_article'},
#             {'title': 'Обратная связь', 'url_name': 'contact'},
#             {'title': 'Войти', 'url_name': 'login'}]

#     return menu
