from django.db import models

from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
        username = None
        email = models.EmailField(unique=True, verbose_name='почта')
        phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
        avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
        city = models.CharField(max_length=40, verbose_name='город', **NULLABLE)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        def __str__(self):
            return self.email

        class Meta:
            verbose_name = "пользователь"
            verbose_name_plural = "пользователи"
