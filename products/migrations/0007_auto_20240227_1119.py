# Generated by Django 3.2.9 on 2024-02-27 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_product_desription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color_variant',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size_variant',
        ),
        migrations.DeleteModel(
            name='ColorVariant',
        ),
        migrations.DeleteModel(
            name='SizeVariant',
        ),
    ]
