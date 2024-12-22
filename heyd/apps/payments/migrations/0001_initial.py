# Generated by Django 5.1.3 on 2024-12-22 10:50

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requests', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='requests.projectrequest')),
            ],
        ),
    ]
