# Generated by Django 4.1.4 on 2022-12-23 19:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Chat_App', '0004_remove_messages_timesent_messages_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='timeSent',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
