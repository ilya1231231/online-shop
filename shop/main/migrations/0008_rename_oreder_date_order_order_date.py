# Generated by Django 3.2.5 on 2021-08-05 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210805_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='oreder_date',
            new_name='order_date',
        ),
    ]