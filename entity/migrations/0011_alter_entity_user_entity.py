# Generated by Django 3.2.9 on 2022-05-20 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0010_alter_entity_user_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity_user',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.entity'),
        ),
    ]