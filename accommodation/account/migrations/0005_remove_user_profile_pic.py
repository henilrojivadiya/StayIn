# Generated by Django 3.0.8 on 2020-12-30 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
    ]
