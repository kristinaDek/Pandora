# Generated by Django 3.0.2 on 2020-08-28 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200826_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='available',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.AvailabilityModel'),
        ),
    ]
