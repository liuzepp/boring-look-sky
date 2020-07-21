# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Goodshow', '0001_initial'),
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='Goodshow.GoodsInfo')),
                ('user', models.ForeignKey(to='Login.User')),
            ],
        ),
    ]
