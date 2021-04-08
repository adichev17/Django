from django.db import models

from django.urls import reverse

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название:')
    content = models.TextField(blank=True, verbose_name='Текст:')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True, verbose_name='Фотография:')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')# connect models Category. models.PROTECT при удалении категории не даст удалить новости.
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id": self.pk}) #выстраиваем маршрут. reverse тоже самое что url в html file

    def __str__(self): #При возвращении модели её наименование будет title (for method News.objects.all())
        return self.title

    class Meta:
        verbose_name = 'Новость' #Измнение заголовка в админке
        verbose_name_plural = 'Новости' #Измнение заголовка в админке
        ordering = ['-created_at'] # sort news.

class Category(models.Model):
    title = models.CharField(max_length=100, db_index= True, verbose_name= 'Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk}) #выстраиваем маршрут. reverse тоже самое что url в html file


    def __str__(self): #При возвращении модели её наименование будет title (for method News.objects.all())
        return self.title

    class Meta:
        verbose_name = 'Категория' #Измнение заголовка в админке
        verbose_name_plural = 'Категории' #Измнение заголовка в админке
        ordering = ['title'] # sort news.