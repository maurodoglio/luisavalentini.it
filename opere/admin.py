from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Mostra, Opera


@admin.register(Mostra)
class MostraAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('beginning', 'name', 'mostra_description', 'type')
    search_fields = ['name', 'content']
    list_filter = ('published', 'type')
    ordering = ('-beginning', 'name', 'type')

    @admin.display(description='Descrizione')
    def mostra_description(self, obj):
        return mark_safe(obj.content)


@admin.register(Opera)
class OperaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('opera_thumb', 'title', 'typology', 'opera_description', 'creation_year')
    search_fields = ['title', 'content']
    list_filter = ('typology', 'published', 'creation_year')

    @admin.display(description='Immagine')
    def opera_thumb(self, obj):
        if obj.thumb:
            return format_html('<img src="{}" alt="{}" style="max-height:50px">', obj.thumb.url, obj.title)
        return '-'

    @admin.display(description='Descrizione')
    def opera_description(self, obj):
        return mark_safe(obj.content)
