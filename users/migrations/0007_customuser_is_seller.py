# Generated by Django 3.1.6 on 2021-03-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210310_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_seller',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]