# Generated by Django 3.1.1 on 2020-09-24 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('site_settings', '0002_auto_20200924_1630'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SocialMediaSetting',
            new_name='SocialMediaSettings',
        ),
    ]
