# Generated by Django 4.2.4 on 2023-08-31 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantsApp', '0008_remove_restaurant_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='average_rating',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
