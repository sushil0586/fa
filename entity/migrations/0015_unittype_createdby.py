# Generated by Django 4.0.4 on 2022-05-25 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entity', '0014_alter_entity_user_createdby'),
    ]

    operations = [
        migrations.AddField(
            model_name='unittype',
            name='createdby',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]