from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .genre import Genre
from .mixins import TimeStampedMixin, UUIDMixin
from .person import Person


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Модель кинопроизведения."""

    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('Tv show')

    title = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), null=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
    ])
    type = models.CharField(_('type'), choices=Type.choices, max_length=60)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork', verbose_name=_('genres'))
    persons = models.ManyToManyField(Person, through='PersonFilmwork', verbose_name=_('persons'))

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')

    def __str__(self):
        return self.title
