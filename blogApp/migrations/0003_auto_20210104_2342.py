# Generated by Django 3.1.4 on 2021-01-04 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0002_auto_20210104_2341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='blog_image',
            new_name='thumbnail',
        ),
    ]
