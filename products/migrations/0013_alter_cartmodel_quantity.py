# Generated by Django 5.0.3 on 2024-03-16 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_cartmodel_finall_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='quantity',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
