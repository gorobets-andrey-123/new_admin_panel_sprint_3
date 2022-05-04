"""Общие для всех моделей свойства."""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    """Базовый класс с описание поля id."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    """Базовый класс с временными метками модели."""

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True
