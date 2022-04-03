from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from .models import Women, Category


@admin.register(Women)
class WomenAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'category', 'time_create', 'time_update', 'get_html_photo', 'is_published'
    )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('category', 'is_published',)
    list_filter = ('category', 'time_create', 'time_update', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'title', 'slug', 'category', 'photo', 'get_html_photo', 'is_published', 'time_create',
        'time_update'
    )
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='100'")

    get_html_photo.short_description = 'Миниатюра'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


admin.site.site_title = 'Админ-панель сайта от Макса'
admin.site.site_header = 'Админ-панель сайта от Макса'
