# Generated by Django 3.2.9 on 2022-05-22 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0013_auto_20220522_1301'),
        ('financial', '0003_account_entity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0003_salesoderheader_entity'),
    ]

    operations = [
        migrations.CreateModel(
            name='purchaseorder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('VoucherDate', models.DateField(auto_now_add=True, verbose_name='Vocucher Date')),
                ('VoucherNo', models.IntegerField(verbose_name='Voucher No')),
                ('BillNo', models.IntegerField(verbose_name='Bill No')),
                ('BillDate', models.DateField(auto_now_add=True, verbose_name='Bill Date')),
                ('Terms', models.BooleanField(verbose_name='Terms')),
                ('TaxType', models.IntegerField(verbose_name='TaxType')),
                ('BillCash', models.IntegerField(verbose_name='Bill/Cash')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Sub Total')),
                ('Cgst', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='C.GST')),
                ('Sgst', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='S.GST')),
                ('Igst', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='I.GST')),
                ('Expenses', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Expenses')),
                ('GTotal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='G Total')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financial.account')),
                ('createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.entity', verbose_name='entity')),
            ],
            options={
                'ordering': ('created_at',),
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='salesorderdetails',
            name='salesOrderHeader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salesOrderdetails', to='invoice.salesoderheader', verbose_name='Sale Order Number'),
        ),
        migrations.CreateModel(
            name='PurchaseOrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Orderqty', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Order Qty')),
                ('pieces', models.IntegerField(verbose_name='pieces')),
                ('Rate', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rate')),
                ('Amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('CSGT', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='CGST')),
                ('SGST', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='SGST')),
                ('IGST', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IGST')),
                ('HSNNo', models.CharField(max_length=255, verbose_name='HSN No')),
                ('LineTotal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Line Total')),
                ('createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.entity', verbose_name='entity')),
                ('purchaseOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PurchaseOrderDetails', to='invoice.purchaseorder', verbose_name='Purchase Order Number')),
            ],
            options={
                'ordering': ('created_at',),
                'abstract': False,
            },
        ),
    ]