# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_auto_20170306_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posting',
            name='item',
        ),
        migrations.RemoveField(
            model_name='posting',
            name='item_category',
        ),
        migrations.RemoveField(
            model_name='posting',
            name='item_description',
        ),
        migrations.RemoveField(
            model_name='posting',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='posting',
            name='address',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='posting',
            name='category',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='posting',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='posting',
            name='title',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='posting',
            name='email',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='posting',
            name='name',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='posting',
            name='phone',
            field=models.TextField(default=b''),
        ),
    ]
