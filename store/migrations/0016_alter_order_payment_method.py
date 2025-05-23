# Generated by Django 4.2 on 2025-05-06 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_order_order_status_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('COD', 'Thanh toán khi nhận hàng'), ('ZaloPay', 'ZaloPay'), ('Momo', 'Ví MoMo'), ('BankTransfer', 'Chuyển khoản ngân hàng'), ('PayOS', 'PayOS')], default=None, max_length=100, null=True),
        ),
    ]
