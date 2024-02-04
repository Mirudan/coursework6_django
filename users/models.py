from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True, 'blank': True
}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    is_active = models.BooleanField(default=False, verbose_name='статус активности')

    email_verify_token = models.CharField(max_length=50, **NULLABLE,
                                          verbose_name='код верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ('is_active',)
        permissions = [
            ('can_block_user', 'Может блокировать пользователя'),
        ]
