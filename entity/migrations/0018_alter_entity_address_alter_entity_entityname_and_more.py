# Generated by Django 4.0.4 on 2022-05-28 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0017_remove_entity_createdby_alter_entity_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='entityName',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='ownerName',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='unitType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Unittype', to='entity.unittype'),
        ),
    ]
