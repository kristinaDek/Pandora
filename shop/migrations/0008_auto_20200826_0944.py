# Generated by Django 3.0.2 on 2020-08-26 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_delete_checkmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='available',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='product',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='productimagemodel',
            name='product',
        ),
        migrations.DeleteModel(
            name='AvailabilityModel',
        ),
        migrations.DeleteModel(
            name='OrderModel',
        ),
        migrations.DeleteModel(
            name='ProductImageModel',
        ),
        migrations.DeleteModel(
            name='ProductModel',
        ),
    ]
