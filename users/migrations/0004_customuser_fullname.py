# Generated by Django 3.1.6 on 2021-03-23 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='fullname',
            field=models.CharField(default='le thanh tu', max_length=70),
            preserve_default=False,
        ),
    ]
