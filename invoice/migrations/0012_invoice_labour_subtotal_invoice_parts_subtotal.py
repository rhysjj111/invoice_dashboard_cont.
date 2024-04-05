# Generated by Django 4.2.11 on 2024-04-02 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_alter_labour_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='labour_subtotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='parts_subtotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]