# Generated by Django 3.2.8 on 2021-10-11 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth0login', '0005_alter_ticket_ticketcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='likeCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='media',
            name='viewCount',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='TOUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affi', models.CharField(max_length=60)),
                ('position', models.CharField(max_length=40)),
                ('zip', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('viewcount', models.ManyToManyField(to='auth0login.MediaViewCount')),
            ],
        ),
        migrations.AddField(
            model_name='mediaviewcount',
            name='media',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='auth0login.media'),
        ),
    ]
