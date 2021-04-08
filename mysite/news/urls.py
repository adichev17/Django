from django.urls import path

from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    #path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('', cache_page(60)(HomeNews.as_view()), name='home'), #.as_view() встроенный метод класса HomeNews
    # path('category/<int:category_id>/', get_category, name='category'),#category_id динамический параметр
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
]