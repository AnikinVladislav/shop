# Generated by Django 4.2.1 on 2023-05-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(),
        ),
    ]
