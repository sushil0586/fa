# Generated by Django 3.2.9 on 2022-05-20 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0008_auto_20220520_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity_user',
            name='entity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='entity.entity'),
        ),
    ]