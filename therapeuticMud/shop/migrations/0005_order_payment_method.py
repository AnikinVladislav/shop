# Generated by Django 4.2.1 on 2023-05-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[(0, 'Наличный расчет'), (1, 'Безналичный расчет')], default=1, max_length=1),
        ),
    ]