# Generated by Django 5.1.1 on 2024-09-13 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='is_publiс',
            field=models.BooleanField(default=False, verbose_name='Общедоступность'),
        ),
    ]
