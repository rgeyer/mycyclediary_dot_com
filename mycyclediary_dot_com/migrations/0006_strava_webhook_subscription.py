# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-15 03:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycyclediary_dot_com', '0005_auto_20160225_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='strava_webhook_subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strava_id', models.PositiveSmallIntegerField()),
                ('object_type', models.CharField(max_length=255)),
                ('aspect_type', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]