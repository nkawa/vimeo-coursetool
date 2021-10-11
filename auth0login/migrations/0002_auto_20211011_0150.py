# Generated by Django 3.2.8 on 2021-10-10 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('auth0login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('vid', models.CharField(max_length=10)),
                ('lecturer', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticketCount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group')),
                ('mlist', models.ManyToManyField(to='auth0login.Media')),
            ],
        ),
    ]
