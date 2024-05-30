# Generated by Django 5.0.6 on 2024-05-30 14:28

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.CharField(max_length=500)),
                ('normalized_msg_text', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('send_date', models.DateTimeField(default=None, verbose_name='date send')),
                ('received_date', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='date received')),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['send_date'],
            },
        ),
    ]