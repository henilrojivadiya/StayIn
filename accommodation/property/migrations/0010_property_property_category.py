# Generated by Django 3.0.8 on 2020-12-21 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_property_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_category', to='property.Property_Category'),
        ),
    ]
