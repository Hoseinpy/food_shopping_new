# Generated by Django 5.0.3 on 2024-03-16 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0003_remove_usermodel_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='user/avatar'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='bio',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
