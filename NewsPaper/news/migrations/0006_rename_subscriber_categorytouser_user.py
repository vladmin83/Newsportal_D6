# Generated by Django 4.0.3 on 2022-04-09 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_categorytouser_category_subscribers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categorytouser',
            old_name='subscriber',
            new_name='user',
        ),
    ]
