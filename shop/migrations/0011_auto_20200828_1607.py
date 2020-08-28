# Generated by Django 3.0.2 on 2020-08-28 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20200828_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='available',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.AvailabilityModel'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ProductModel'),
        ),
    ]
