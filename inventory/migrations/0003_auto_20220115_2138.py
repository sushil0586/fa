# Generated by Django 3.2.9 on 2022-01-15 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_product_openingstockbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='OpeningStock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='openingStockBox',
        ),
        migrations.AddField(
            model_name='product',
            name='Mrp',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='M.R.P'),
        ),
        migrations.AddField(
            model_name='product',
            name='MrpLess',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Less %'),
        ),
        migrations.AddField(
            model_name='product',
            name='OpeningStockqty',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Opening Stock Qty'),
        ),
        migrations.AddField(
            model_name='product',
            name='OpeningStockvalue',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Opening Stock Value'),
        ),
        migrations.AddField(
            model_name='product',
            name='PRlessPercentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Less %'),
        ),
        migrations.AddField(
            model_name='product',
            name='Purchaserate',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Purchase Rate'),
        ),
        migrations.AddField(
            model_name='product',
            name='SalePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Sale Price'),
        ),
        migrations.AddField(
            model_name='product',
            name='Totalgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Less %'),
        ),
        migrations.AddField(
            model_name='product',
            name='cgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='C GST @'),
        ),
        migrations.AddField(
            model_name='product',
            name='cgstcess',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Cess Qty'),
        ),
        migrations.AddField(
            model_name='product',
            name='openingStockBoxqty',
            field=models.IntegerField(blank=True, default=True, verbose_name='Box/Pcs'),
        ),
        migrations.AddField(
            model_name='product',
            name='sgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='S GST @'),
        ),
        migrations.AddField(
            model_name='product',
            name='sgstcess',
            field=models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, verbose_name='Cess Qty'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ProductDesc',
            field=models.TextField(verbose_name='Product Desc'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ProductName',
            field=models.CharField(max_length=255, verbose_name='Product Name'),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('PCategoryName', models.CharField(max_length=255, verbose_name='Product Category')),
                ('MainCategory', models.ForeignKey(blank=True, default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.productcategory', verbose_name='Main category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='ProductCategory',
            field=models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.productcategory', verbose_name='Product Category'),
        ),
    ]
