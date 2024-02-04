from django.db import models
from django.db.models import ForeignKey

from clients.models import Client
from config import settings

from users.models import NULLABLE


class MailingMessage(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(**NULLABLE, verbose_name='тело письма')
    recipient = models.ManyToManyField(Client, related_name='clients', verbose_name='клиенты')
    is_published = models.BooleanField(default=True, verbose_name='опубликована')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='mails', related_query_name="mail",
                              **NULLABLE, verbose_name='автор рассылки')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('owner', 'is_published')
        permissions = [
            ('can_cancel_mailing', 'Может отменять публикацию рассылки'),
        ]


class MailingSettings(models.Model):
    class FREQUENCY(models.TextChoices):
        DAILY = 'daily', 'Ежедневно'
        WEEKLY = 'weekly', 'Еженедельно'
        MONTHLY = 'monthly', 'Ежемесячно'

    class STATUS(models.TextChoices):
        CREATED = 'created', 'Создана'
        RUNNING = 'running', 'Запущена'
        COMPLETED = 'completed', 'Завершена'

    message = ForeignKey(MailingMessage, on_delete=models.CASCADE,
                         related_name='settings', related_query_name="setting",
                         verbose_name='рассылка')
    mailing_start = models.DateField(**NULLABLE, verbose_name='начало рассылки')
    mailing_end = models.DateField(**NULLABLE, verbose_name='конец рассылки')
    mailing_period = models.CharField(max_length=12, choices=FREQUENCY.choices,
                                      **NULLABLE, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=10, choices=STATUS.choices,
                                      default='created', verbose_name='статус рассылки')
    next_sending_date = models.DateField(**NULLABLE, verbose_name='следующая отправка')

    def __str__(self):
        return f'{self.mailing_start} - {self.mailing_end}'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылки'
        ordering = ('mailing_start', 'mailing_end',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next_sending_date:
            self.next_sending_date = self.mailing_start

    def save(self, *args, **kwargs):
        if not self.next_sending_date:
            self.next_sending_date = self.mailing_start
        super().save(*args, **kwargs)

    def get_mailing_status_display(self):
        return dict(self.STATUS.choices).get(self.mailing_status, 'Черновик')

    def get_mailing_period_display(self):
        return dict(self.FREQUENCY.choices).get(self.mailing_period, 'Не указано')


class MailingLog(models.Model):
    class STATUS(models.TextChoices):
        SUCCESS = 'Успешно'
        FAILED = 'Неуспешно'

    status = models.CharField(max_length=9, choices=STATUS.choices, **NULLABLE, verbose_name='статус отправки')
    message = models.TextField(**NULLABLE, verbose_name='ответ сервера')
    date = models.DateTimeField(**NULLABLE, verbose_name='время попытки')
    mailing = models.ForeignKey(MailingMessage, **NULLABLE, on_delete=models.SET_NULL, verbose_name='рассылка')

    def __str__(self):
        return f'{self.date} - {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('status',)
