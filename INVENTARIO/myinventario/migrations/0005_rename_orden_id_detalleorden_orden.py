# Generated by Django 4.2.7 on 2023-11-30 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myinventario', '0004_rename_producto_id_detalleorden_producto_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalleorden',
            old_name='orden_id',
            new_name='orden',
        ),
    ]