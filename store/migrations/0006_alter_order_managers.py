# Generated by Django 4.1 on 2022-09-02 13:24

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_managers_alter_order_order_key_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('orders', django.db.models.manager.Manager()),
            ],
        ),
    ]