from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    # path('', cache_page(60)(views.ListArticles.as_view()), name='home'),
    path('', views.ListArticles.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addrticle/', views.AddArticle.as_view(), name='add_article'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('post/<slug:slug>/', views.ShowArticle.as_view(), name='post'),
    path('category/<slug:slug>/', views.CategoryArticlesList.as_view(), name='category'),
]
