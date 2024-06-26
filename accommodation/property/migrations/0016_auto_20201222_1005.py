# Generated by Django 3.0.8 on 2020-12-22 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0015_auto_20201221_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('iframe_map_link', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': '(13) Area',
            },
        ),
        migrations.RemoveField(
            model_name='property',
            name='iframe_map_link',
        ),
        migrations.AlterField(
            model_name='property',
            name='property_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Property_Category'),
        ),
        migrations.AddField(
            model_name='property',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Area'),
        ),
    ]
