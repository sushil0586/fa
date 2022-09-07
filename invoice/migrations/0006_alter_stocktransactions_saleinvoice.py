# Generated by Django 4.1 on 2022-08-17 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_stocktransactions_saleinvoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocktransactions',
            name='saleinvoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.salesoderheader', verbose_name='sale invoice no'),
        ),
    ]