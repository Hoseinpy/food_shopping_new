# Generated by Django 5.0.3 on 2024-03-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_cartmodel_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmodel',
            name='finall_price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
    ]