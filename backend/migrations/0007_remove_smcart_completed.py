# Generated by Django 4.2 on 2023-04-29 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_family_has_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smcart',
            name='completed',
        ),
    ]
