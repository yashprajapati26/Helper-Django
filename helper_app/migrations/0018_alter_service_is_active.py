# Generated by Django 4.1 on 2022-08-24 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper_app', '0017_service_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
