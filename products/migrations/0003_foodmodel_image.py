# Generated by Django 5.0.3 on 2024-03-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_foodcategory_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='food'),
        ),
    ]
