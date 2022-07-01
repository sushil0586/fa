# Generated by Django 3.2.9 on 2022-05-20 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entity', '0005_alter_entityuser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entityuser',
            name='createdby',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='entityuser_requests_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entityuser',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]