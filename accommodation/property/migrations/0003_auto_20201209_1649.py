# Generated by Django 3.0.8 on 2020-12-09 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('owner', '0001_initial'),
        ('property', '0002_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('icon', models.ImageField(upload_to='icon/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Amenities',
                'verbose_name_plural': '(8) Amenities',
            },
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Policies',
                'verbose_name_plural': '(9) Policies',
            },
        ),
        migrations.CreateModel(
            name='Popular_Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Popular Location',
                'verbose_name_plural': '(5) Popular Locations',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=400)),
                ('price', models.IntegerField()),
                ('deposite', models.IntegerField()),
                ('total_room', models.IntegerField(default=0)),
                ('avail_space_per_room', models.IntegerField(default=0)),
                ('total_space', models.IntegerField()),
                ('available_space', models.IntegerField()),
                ('description', models.TextField()),
                ('iframe_map_link', models.CharField(max_length=900)),
                ('is_verify', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='owner.Owner')),
                ('popular_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='popular_location', to='property.Popular_Location')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': '(1) Properties',
            },
        ),
        migrations.CreateModel(
            name='Property_For',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Property For',
                'verbose_name_plural': '(7) Property For',
            },
        ),
        migrations.CreateModel(
            name='Property_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Property Type',
                'verbose_name_plural': '(6) Property Types',
            },
        ),
        migrations.CreateModel(
            name='Property_Wise_Policies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('policy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Policies')),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Property')),
            ],
            options={
                'verbose_name': 'Property Wise Policies',
                'verbose_name_plural': '(3) Property Wise Policies',
            },
        ),
        migrations.CreateModel(
            name='Property_Wise_Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amenities', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Amenities')),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Property')),
            ],
            options={
                'verbose_name': 'Property Wise Amenities',
                'verbose_name_plural': '(2) Properties Wise Amenities',
            },
        ),
        migrations.CreateModel(
            name='Property_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, upload_to='property_images/')),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Property')),
            ],
            options={
                'verbose_name': 'Property Images',
                'verbose_name_plural': '(4) Property Wise Images',
            },
        ),
        migrations.AddField(
            model_name='property',
            name='property_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_for', to='property.Property_For'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_type', to='property.Property_Type'),
        ),
    ]
