from django import template
from django.db.models import Count, F

from news.models import Category

register = template.Library() #Регестрируем наш template tag

#Декораторы - возможность отменить поведение функции
@register.simple_tag(name = 'get_list_categories') #Чтобы облегчить создание тегов этого типа, Django предоставляет служебную функцию simple_tag . Эта функция, которая является методом django.template.Library , сама принимает функцию, которая принимает столько параметров, сколько необходимо, превращает ее в функцию render вместе с другими необходимыми элементами, как указано выше, и регистрирует ее в системе шаблонов. ,
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html') #рендерим шаблон.Другой распространенный тип тега набора элементов - это тип, который отображает определенные данные при визуализации другого набора элементов . Например, интерфейс администратора Django использует настраиваемые теги шаблонов для отображения кнопок внизу страниц добавления / редактирования форм. Эти кнопки всегда выглядят одинаково, но цели их ссылок меняются в зависимости от редактируемого объекта, поэтому они представляют собой типичный случай использования небольшого шаблона, дополненного некоторыми подробностями об редактируемом объекте.
def show_categories():
    #categories = Category.objects.all()
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)# не отображаем пустые категории
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)  # не отображаем пустые категории
    return {"categories": categories} #отдаём в него данные