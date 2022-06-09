# Generated by Django 4.0.4 on 2022-06-05 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('CountryName', models.CharField(max_length=255)),
                ('CountryCode', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='state',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('StateName', models.CharField(max_length=255)),
                ('StateCode', models.CharField(max_length=25)),
                ('Country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='geography.country')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='district',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('districtName', models.CharField(max_length=255)),
                ('districtCode', models.CharField(max_length=25)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district', to='geography.state')),
            ],
            options={
                'ordering': ('created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cityName', models.CharField(max_length=255)),
                ('cityCode', models.CharField(max_length=25)),
                ('distt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='geography.district')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
    ]
