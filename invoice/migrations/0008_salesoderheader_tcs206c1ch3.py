# Generated by Django 4.1 on 2022-08-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_remove_salesoderheader_tcs206c1ch3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesoderheader',
            name='tcs206c1ch3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tcs tcs206c1ch3'),
        ),
    ]
