from django.core.management import BaseCommand
import datetime

from materials.models import Course, Lesson
from users.models import Payments


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        payment1 = Payments.objects.create(
            date_of_payment=datetime.datetime.now().date(),
            amount=30000,
            payment_type='cash',
            payed_course=Course.objects.get(pk=2),
        )

        payment2 = Payments.objects.create(
            date_of_payment=datetime.datetime.now().date(),
            amount=500,
            payment_type='card',
            payed_lesson=Lesson.objects.get(pk=1),
        )

        payment1.save()
        payment2.save()