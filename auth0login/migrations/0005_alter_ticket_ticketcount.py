# Generated by Django 3.2.8 on 2021-10-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth0login', '0004_media_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticketCount',
            field=models.IntegerField(default=0),
        ),
    ]
