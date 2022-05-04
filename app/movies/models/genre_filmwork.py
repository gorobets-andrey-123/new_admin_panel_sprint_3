from django.db import models
from django.utils.translation import gettext_lazy as _

from .genre import Genre
from .mixins import UUIDMixin


class GenreFilmwork(UUIDMixin):
    """Связи многие-ко-многим жанра с кинопроизведением."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('filmwork'))
    genre: Genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        indexes = (
            models.Index(fields=['film_work', 'genre']),
        )

    def __str__(self):
        return self.genre.name
