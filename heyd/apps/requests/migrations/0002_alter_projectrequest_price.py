# Generated by Django 5.1.4 on 2024-12-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrequest',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=40, null=True),
        ),
    ]
