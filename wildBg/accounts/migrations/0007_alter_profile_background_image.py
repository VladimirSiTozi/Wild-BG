# Generated by Django 5.1.3 on 2024-12-11 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_level_alter_profile_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='background_images/'),
        ),
    ]