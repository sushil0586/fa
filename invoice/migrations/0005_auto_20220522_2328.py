# Generated by Django 3.2.9 on 2022-05-22 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20220522_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseorderdetails',
            options={},
        ),
        migrations.RemoveField(
            model_name='purchaseorderdetails',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='purchaseorderdetails',
            name='updated_at',
        ),
    ]
