# Generated by Django 5.1.3 on 2024-12-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_post_tagged_people'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default=1, upload_to='posts/'),
            preserve_default=False,
        ),
    ]