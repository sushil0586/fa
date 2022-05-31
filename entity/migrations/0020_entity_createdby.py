# Generated by Django 4.0.4 on 2022-05-29 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entity', '0019_alter_entity_address_alter_entity_entityname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='createdby',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]