from django.core import mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator #постраничная навигация

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  #auth.
            return redirect('home')
    else:
            form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def contact(request): #send mail
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['сontent'], 'adichev19@mail.ru', ['adichev17@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})
# Create your views here.

#Переопределяем атрибуты класса ListView или класса выше
class HomeNews(ListView): # analog def index(request)
    model = News # аналог news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news' #change object_list on news.
    #extra_context = {'title': 'Главная'}
    mixin_prop = 'hello world'
    paginate_by = 2 #кол-во новостей на одной странице

    def get_context_data(self, *, object_list=None, **kwargs): #Аналог extra_context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self): #for filter data. Views only is_published=True
        return News.objects.filter(is_published=True).select_related('category') #.select_related используется для оптимизации запросов.Метод сразу подгружает данные ан еждёт их запроса!

class NewsByCategory(ListView): #Аналог extra_context def get_category(request, category_id)
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False #Block empty list
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs): #Аналог extra_context
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

class ViewNews(DetailView):# analog def view_news(request, news_id):
    model = News
    pk_url_kwarg = 'news_id'
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'

class CreateNews(LoginRequiredMixin ,CreateView): # analog def add_news(request)
    form_class = NewsForm #connect
    template_name = 'news/add_news.html'
    #Редирект на созданную новость просходит из-за метода в models.py def get_absolute_url(self)
    #Пример редиректа на главную страницу
    #success_url = reverse_lazy('home')
    login_url = '/admin/'





# def index(request):
#     #print(request)
#     news = News.objects.all()
#     return render(request, 'news/index.html', {'news': news, 'title': 'Список новостей'})

# def get_category(request, category_id): #Формируем новости по категориям
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})

# def view_news(request, news_id):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST) #отправка формы
#         if form.is_valid():
#             #print(form.cleaned_data)#если форма прошла валидацю то все данные попадают в cleaned_data
#             #news = News.objects.create(**form.cleaned_data) # **распаковка словаря. Используется в формах не связанными с моделями
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})