from django.db import models

from config import settings
from users.models import NULLABLE


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=255, **NULLABLE, verbose_name='комментарий')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='cleints', related_query_name='client',
                              **NULLABLE, verbose_name='владелец списка рассылки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'клиент рассылки'
        verbose_name_plural = 'клиенты рассылки'
        ordering = ('email',)
