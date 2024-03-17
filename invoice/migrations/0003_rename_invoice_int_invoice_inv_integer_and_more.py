# Generated by Django 4.2.11 on 2024-03-17 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_part_labour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='invoice_int',
            new_name='inv_integer',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='invoice_number',
            new_name='inv_number',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='sub_total',
            new_name='subtotal',
        ),
        migrations.AddField(
            model_name='invoice',
            name='vat_subtotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labour',
            name='subtotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='subtotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
