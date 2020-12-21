# Generated by Django 3.1.3 on 2020-12-21 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0021_auto_20201221_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='user',
        ),
        migrations.AddField(
            model_name='productreview',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.profile'),
            preserve_default=False,
        ),
    ]
