# Generated by Django 4.1 on 2022-08-30 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0015_purchasereturn_advance_purchasereturn_tds194q1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesoderheader',
            name='latepaymentalert',
            field=models.BooleanField(default=True, null=True, verbose_name='Late Payment Alert'),
        ),
    ]
