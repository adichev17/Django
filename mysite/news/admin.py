from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from django import forms
from .models import News, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class NewsPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = NewsPostAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo') #для отображения в соотв.порядке в админке заголовка влкадок новостец
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'created_at', 'views', 'updated_at')
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')

    def get_photo(self, obj): # view photo in admin panel
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width = "75">')#помечает данную строку как html строку и не экранирует её
        else:
            return 'Фото не установлено'

    get_photo.short_description = 'Фотография' #изменяем имя в админ панели


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title') #для отображения в соотв.порядке в админке заголовка влкадок новостец
    list_display_links = ('id', 'title')
    search_fields = ('title',) # (,) тк КОРТЕЖ

admin.site.register(News, NewsAdmin) #Передача модели в админку и её настроки(вторым параметром)
admin.site.register(Category, CategoryAdmin)

