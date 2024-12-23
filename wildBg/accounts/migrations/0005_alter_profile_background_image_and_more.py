# Generated by Django 5.1.3 on 2024-12-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background_image',
            field=models.ImageField(upload_to='background_images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
