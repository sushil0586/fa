# Generated by Django 3.2.9 on 2022-01-10 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('entityName', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('ownerName', models.CharField(max_length=255)),
                ('phoneoffice', models.IntegerField(null=True)),
                ('phoneResidence', models.IntegerField(null=True)),
                ('panno', models.CharField(max_length=255, null=True)),
                ('tds', models.CharField(max_length=255, null=True)),
                ('tdsCircle', models.CharField(max_length=255, null=True)),
                ('Country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geography.country')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geography.city')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geography.district')),
                ('owner', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geography.state')),
            ],
            options={
                'ordering': ('created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='unitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UnitName', models.CharField(max_length=255)),
                ('UnitDesc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='entity_details',
            fields=[
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='entity.entity')),
                ('style', models.CharField(max_length=255, null=True)),
                ('commodity', models.CharField(max_length=255, null=True)),
                ('weightDecimal', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=24, null=True)),
                ('registrationno', models.CharField(max_length=255, null=True)),
                ('division', models.CharField(max_length=255, null=True)),
                ('collectorate', models.CharField(max_length=255, null=True)),
                ('range', models.CharField(max_length=255, null=True)),
                ('adhaarudyog', models.CharField(max_length=255, null=True)),
                ('cinno', models.CharField(max_length=255, null=True)),
                ('jobwork', models.CharField(max_length=255, null=True)),
                ('gstno', models.CharField(max_length=255, null=True)),
                ('gstintype', models.CharField(max_length=255, null=True)),
                ('esino', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='unitType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Unittype', to='entity.unittype'),
        ),
    ]
