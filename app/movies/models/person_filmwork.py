from django.db import models
from django.utils.translation import gettext_lazy as _

from .filmwork import Filmwork
from .mixins import UUIDMixin
from .person import Person


class PersonFilmwork(UUIDMixin):
    """Связь многие-ко-многим актера и кинопроизведения."""

    class Role(models.TextChoices):
        DIRECTOR = 'director', _('Director')
        ACTOR = 'actor', _('Actor')
        SCREENWRITER = 'screenwriter', _('Screenwriter')

    film_work: Filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('filmwork'))
    person: Person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('person'))
    role = models.CharField(
            _('role'), choices=Role.choices, null=True, max_length=255,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        unique_together = (('film_work_id', 'person_id'),)

    def __str__(self):
        return '{person} ({role})'.format(person=self.person.full_name, role=self.role)
