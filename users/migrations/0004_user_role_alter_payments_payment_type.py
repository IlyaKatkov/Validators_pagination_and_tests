# Generated by Django 5.0.2 on 2024-02-17 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('member', 'member'), ('moderator', 'moderator')], default='member', max_length=9),
        ),
        migrations.AlterField(
            model_name='payments',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'Наличными'), ('card', 'Перевод по карте')], max_length=50, verbose_name='способ оплаты'),
        ),
    ]
