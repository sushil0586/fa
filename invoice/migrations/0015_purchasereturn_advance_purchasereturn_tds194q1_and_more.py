# Generated by Django 4.1 on 2022-08-29 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
        ('invoice', '0014_salesoderheader_advance'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasereturn',
            name='advance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='advance'),
        ),
        migrations.AddField(
            model_name='purchasereturn',
            name='tds194q1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='TDS 194 @'),
        ),
        migrations.AddField(
            model_name='purchasereturn',
            name='totalgst',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='totalgst'),
        ),
        migrations.AddField(
            model_name='purchasereturn',
            name='totalpieces',
            field=models.IntegerField(blank=True, default=0, verbose_name='totalpieces'),
        ),
        migrations.AddField(
            model_name='purchasereturn',
            name='totalquanity',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='totalquanity'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='accountid',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='financial.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='billno',
            field=models.IntegerField(verbose_name='Bill No'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='broker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker1', to='financial.account'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='grno',
            field=models.CharField(default=1, max_length=50, verbose_name='GR No'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='latepaymentalert',
            field=models.IntegerField(verbose_name='Late Payment Alert'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='shippedto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippedto1', to='financial.account'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='supply',
            field=models.IntegerField(verbose_name='Supply'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='tcs206c1ch3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tcs tcs206c1ch3'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='transport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transport1', to='financial.account'),
        ),
    ]
