# Generated by Django 5.0.3 on 2024-03-16 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_foodcategory_image_alter_foodmodel_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='foodmodel',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
