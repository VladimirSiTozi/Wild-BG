# Generated by Django 5.1.3 on 2024-11-29 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_landmarks_visited'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]