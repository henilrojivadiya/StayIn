# Generated by Django 3.0.8 on 2020-12-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_property_total_bathroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='total_bathroom',
            field=models.IntegerField(default=0),
        ),
    ]