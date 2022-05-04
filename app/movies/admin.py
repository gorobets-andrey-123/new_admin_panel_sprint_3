"""Модуль с конфигурацией админки."""

from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс с правилами обработки модели Genre в адмике."""

    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description', 'id')
    ordering = ('name',)


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    """Класс с правилами обработки модели Person в адмике."""

    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name', 'id')
    ordering = ('full_name',)


class GenreFilmworkInline(admin.TabularInline):
    """Форма жанров на странице редактирования модели Filmwork."""

    model = models.GenreFilmwork
    verbose_name = _('genre')
    verbose_name_plural = _('genres')
    extra = 1


class PersonFilmworkInline(admin.TabularInline):
    """Форма актеров на странице редактирования модели Filmwork."""

    model = models.PersonFilmwork
    verbose_name = _('person')
    verbose_name_plural = _('persons')
    extra = 1
    autocomplete_fields = ('person',)


@admin.register(models.Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Класс с правилами обработки модели Filmwork в админке."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = (
        'title', 'type', 'creation_date', 'rating', 'created', 'modified',
    )

    list_filter = (
        'type',
        AutocompleteFilterFactory(_('genre'), 'genres'),
        AutocompleteFilterFactory(_('person'), 'persons'),
    )

    search_fields = ('title', 'description', 'id')
    ordering = ('title',)
