# Generated by Django 3.0.8 on 2020-12-21 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_auto_20201221_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Landmark',
                'verbose_name_plural': '(12) Landmark',
            },
        ),
        migrations.AlterField(
            model_name='property',
            name='property_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Property_Category'),
        ),
    ]
