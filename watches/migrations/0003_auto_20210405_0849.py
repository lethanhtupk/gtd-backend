# Generated by Django 3.1.6 on 2021-04-05 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watches', '0002_watch_lowest_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='status',
            field=models.CharField(choices=[(1, 'Active'), (2, 'Deactivate')], default=1, max_length=2),
        ),
    ]