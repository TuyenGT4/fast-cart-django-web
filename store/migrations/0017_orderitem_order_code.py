# Generated by Django 4.2 on 2025-05-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
