# Generated by Django 3.0.8 on 2020-12-30 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='profile_pic.svg', upload_to='profile_pic/'),
        ),
    ]