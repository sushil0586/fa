# Generated by Django 4.0.4 on 2022-05-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0004_alter_accounthead_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounthead',
            name='balanceType',
            field=models.CharField(max_length=50, null=True, verbose_name='Balance Type'),
        ),
    ]
