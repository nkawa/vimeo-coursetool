# Generated by Django 3.2.8 on 2021-10-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth0login', '0002_auto_20211011_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='theme',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='media',
            name='lecturer',
            field=models.CharField(max_length=60),
        ),
    ]