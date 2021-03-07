# Generated by Django 3.1.6 on 2021-03-04 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watches', '0013_watch_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watches', to=settings.AUTH_USER_MODEL),
        ),
    ]
