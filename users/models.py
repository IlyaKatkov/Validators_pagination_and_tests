from django.db import models

from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}



class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')

class User(AbstractUser):
        username = None
        email = models.EmailField(unique=True, verbose_name='почта')
        phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
        avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
        city = models.CharField(max_length=40, verbose_name='город', **NULLABLE)
        role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        def __str__(self):
            return self.email

        class Meta:
            verbose_name = "пользователь"
            verbose_name_plural = "пользователи"

class Payments(models.Model):
    class PaymentsType(models.TextChoices):
        CASH = 'cash', 'Наличными'
        BANK = 'card', 'Перевод по карте'

    payer = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='плательщик', related_name='payer')
    date_of_payment = models.DateField(auto_now=True, verbose_name='дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплаченный курс')
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='сумма оплаты')
    payment_type = models.CharField(max_length=50, choices=PaymentsType.choices, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.payer} - {self.payed_course if self.payed_course else self.payed_lesson} - {self.amount}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
