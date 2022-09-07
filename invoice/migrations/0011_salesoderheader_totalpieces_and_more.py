# Generated by Django 4.1 on 2022-08-25 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
        ('invoice', '0010_alter_salesoderheader_broker_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesoderheader',
            name='totalpieces',
            field=models.IntegerField(blank=True, default=0, verbose_name='pieces'),
        ),
        migrations.AddField(
            model_name='salesoderheader',
            name='totalweight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='totalweight'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='accountid',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='financial.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='billcash',
            field=models.IntegerField(verbose_name='Bill/Cash'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='billno',
            field=models.IntegerField(verbose_name='Bill No'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='broker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker', to='financial.account'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='grno',
            field=models.CharField(default=1, max_length=50, verbose_name='GR No'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='latepaymentalert',
            field=models.IntegerField(verbose_name='Late Payment Alert'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='shippedto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippedto', to='financial.account'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='supply',
            field=models.IntegerField(verbose_name='Supply'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='taxtype',
            field=models.IntegerField(verbose_name='Tax Type'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='tcs206c1ch3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tcs tcs206c1ch3'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='terms',
            field=models.IntegerField(verbose_name='Terms'),
        ),
        migrations.AlterField(
            model_name='salesoderheader',
            name='transport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transport', to='financial.account'),
        ),
        migrations.AlterField(
            model_name='stocktransactions',
            name='creditamount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Credit Amount'),
        ),
        migrations.AlterField(
            model_name='stocktransactions',
            name='debitamount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Debit Amount'),
        ),
    ]