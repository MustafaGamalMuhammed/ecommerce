# Generated by Django 3.1.3 on 2020-11-29 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_product_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='ecommerce.cart'),
        ),
    ]
