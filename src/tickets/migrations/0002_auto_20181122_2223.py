# Generated by Django 2.1.3 on 2018-11-22 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='admin',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_in_chat', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_in_chat', to=settings.AUTH_USER_MODEL),
        ),
    ]