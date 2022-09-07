# Generated by Django 4.1 on 2022-09-01 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0019_salesoderheader_taxid'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasereturn',
            name='taxid',
            field=models.IntegerField(default=0, verbose_name='Terms'),
        ),
        migrations.AlterField(
            model_name='accountentry',
            name='closingbalance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='closing Amount'),
        ),
        migrations.AlterField(
            model_name='accountentry',
            name='openingbalance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Opening Amount'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='closingbalance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='closing Amount'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='openingbalance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Opening Amount'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='latepaymentalert',
            field=models.BooleanField(default=True, null=True, verbose_name='Late Payment Alert'),
        ),
    ]
