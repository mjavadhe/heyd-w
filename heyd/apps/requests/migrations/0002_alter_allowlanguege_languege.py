# Generated by Django 5.1.4 on 2024-12-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowlanguege',
            name='languege',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
