# Generated by Django 5.1.3 on 2024-12-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='national_code',
            field=models.CharField(max_length=10, unique=True, verbose_name='National Code'),
        ),
    ]
