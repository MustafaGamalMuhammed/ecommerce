# Generated by Django 3.1.3 on 2020-11-22 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
