from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .models import Women, Category
from .forms import AddArticleForm, RegisterUserForm, LoginUserForm, ContactForm
from .utils import DataMixin


class ListArticles(DataMixin, ListView):
    """Список всех статей"""

    # укажем число постов на странице, это число элементов списка
    # выводимых на странице
    # paginate_by = 2

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')

        # print(context | c_def)
        # обновляем словарь, как в уроке:
        # return dict(list(context.items()) + list(c_def.items()))

        # а можно обновить словарь так:
        # context.update(c_def)
        # return context

        # но можно обновить и так:
        return context | c_def

        # context['menu'] = menu
        # context['title'] = 'Главная страница'
        # context['category_selected'] = 0
        # return context

    # Отображение только тех статей, которые помечены как опубликованные
    # и возьмет все связанные данные категорий по внешнему ключу Foreignkey:
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('category')


# def index(request):
#     """Главная страница, отображение всех записей"""
#     posts = Women.objects.all()
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'category_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    # для пагинации в функциях представлений для примера:
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    """Добавление статьи"""
    form_class = AddArticleForm
    template_name = 'women/addarticle.html'
    # если в модели я не писал метод get_absolute_url, тогда для
    # перенаправления после создания записи в форме, надо
    # указать куда перенаправлять, например адрес маршрута 'home',
    # именно reverse_lazy позволяет использовать имена маршрутов:
    # success_url = reverse_lazy('home')

    # для перенаправления после авторизации(после применения LoginRequiredMixin)
    # login_url = '<например на страницу login>'
    login_url = reverse_lazy('home')

    # когда не авторизован для того,
    # чтобы генерировалась ошибка 403 доступ запрещен:
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добаление статьи')

        # print(context | c_def)
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        return context | c_def


# если используется функция представления и надо ограничить доступ
# неавторизованным пользователям, надо использовать декоратор:
# например:
# @login_required
# def addarticle(request):
#     """Добавление статьи"""
#     if request.method == 'POST':
#         form = AddArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddArticleForm()

#     context = {
#         'form': form,
#         'title': 'Добавить статью'
#     }
#     return render(request, 'women/addarticle.html', context=context)


class ContactFormView(DataMixin, FormView):
    """Форма обратной связи"""
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def contact(request):
#     return HttpResponse('Обратная связь')


# def login(request):
#     return HttpResponse('Авторизация')


class ShowArticle(DataMixin, DetailView):
    """Читать статью"""
    model = Women
    context_object_name = 'post'
    # чтобы в urls.py прописать не просто <slug:slug>,
    # а например <slug:article_slug>, но article_slug должен возвращать
    # get_absolute_url в модели:
    # slug_url_kwarg = 'article_slug'

    # а если используется не слаг, а атрибут id например то:
    # pk_url_kwarg = 'article_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=context['post'],
            category_selected=context['post'].category_id
        )

        # print(context | c_def)
        # context['title'] = context['post']
        # context['menu'] = menu
        # context['category_selected'] = context['post'].category_id
        return context | c_def


# def show_article(request, slug):
#     """Читать статью"""
#     post = get_object_or_404(Women, slug=slug)
#     context = {
#         'post': post,
#         'title': post.title,
#         'category_selected': post.category_id
#     }
#     return render(request, 'women/post_detail.html', context=context)


class CategoryArticlesList(DataMixin, ListView):
    """Отображение всех статей связанных с выбраной категорией"""
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # если запрашиваемой записи нет(слага нет) в url, то генерируем ошибку 404
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(
            category__slug=self.kwargs['slug'],
            is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        c_def = self.get_user_context(title='Категория - ' + str(category.name),
                                      category_selected=category.pk)

        # print(context | c_def)
        # context['title'] = 'Категория - ' + str(context['posts'][0].category)
        # context['menu'] = menu
        # context['category_selected'] = context['posts'][0].category_id
        return context | c_def


# def show_category(request, slug):
#     """Отображение всех статей связанных с выбраной категорией"""
#     category = Category.objects.get(slug=slug)
#     posts = Women.objects.filter(category=category)

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,
#         'title': category,
#         'category_selected': category.pk
#     }
#     return render(request, 'women/index.html', context=context)


# Будет работать только, когда DEBUG=False
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    """Регистрация"""
    # form_class = UserCreationForm
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    # этот метод вызывается при успешной проверке формы регистрации,
    # если пользователь зарегистрировался на сайте, то
    # сразу автоматически его авторизовываем и перенаправляем:
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    """Авторизация"""
    # form_class = AuthenticationForm
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    # если не прописал константу в settings, то можно добавить этот метод и
    # если пользователь верно ввел логин и пароль, вызовет и перенаправит:
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """Выход из учетной записи"""
    logout(request)
    return redirect('login')



# permanent для указания постоянного перемещения,т.е. кода 301
# def category(request, cat_id):
#     if cat_id > 3:
#         return redirect('home', permanent=True)
#     return HttpResponse('<h1>Статьи по категориям</h1>')
