# Generated by Django 4.2.4 on 2023-08-28 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewsApp', '0002_alter_review_review_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='username',
        ),
    ]
