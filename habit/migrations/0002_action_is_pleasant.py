# Generated by Django 5.1.1 on 2024-09-12 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='is_pleasant',
            field=models.BooleanField(default=False, verbose_name='приятная'),
        ),
    ]
