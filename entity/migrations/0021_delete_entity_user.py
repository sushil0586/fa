# Generated by Django 4.0.4 on 2022-05-29 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0020_entity_createdby'),
    ]

    operations = [
        migrations.DeleteModel(
            name='entity_user',
        ),
    ]