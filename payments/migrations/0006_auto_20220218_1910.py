# Generated by Django 3.2.8 on 2022-02-18 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20220218_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='amount',
            field=models.PositiveIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='invoice',
            name='transaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payments.transaction'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
