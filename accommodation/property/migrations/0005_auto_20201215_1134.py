# Generated by Django 3.0.8 on 2020-12-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_auto_20201209_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(default='Text'),
        ),
        migrations.AlterField(
            model_name='property',
            name='iframe_map_link',
            field=models.CharField(default='Link', max_length=900),
        ),
    ]