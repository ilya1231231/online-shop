# Generated by Django 3.2.5 on 2021-07-31 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210727_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer', verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Общая цена'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес пользователя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона'),
        ),
    ]