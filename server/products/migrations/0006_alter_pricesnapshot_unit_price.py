# Generated by Django 4.2.23 on 2025-07-19 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_pricesnapshot_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricesnapshot',
            name='unit_price',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
