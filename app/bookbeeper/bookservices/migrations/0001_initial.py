# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_date', models.DateTimeField(verbose_name=b'Date of Transaction')),
                ('transaction_type', models.IntegerField(default=1, verbose_name=b'Type of transaction', choices=[(2, b'Subtract from Inventory'), (1, b'Add to Inventory')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LibraryBook',
            fields=[
                ('isbn_13', models.CharField(primary_key=True, serialize=False, max_length=13, unique=True, verbose_name=b'ISBN-13', db_index=True)),
                ('isbn_10', models.CharField(max_length=10, verbose_name=b'ISBN-10', blank=True)),
                ('title', models.CharField(max_length=250, verbose_name=b'Title of book', db_index=True)),
                ('author', models.TextField(max_length=1000, verbose_name=b'Comma-separated lis of authors.')),
                ('publisher', models.CharField(max_length=200, verbose_name=b'Name of imprint or publisher.')),
                ('publish_date', models.PositiveIntegerField(null=True, verbose_name=b'Publication date')),
                ('description', models.TextField(max_length=2000, verbose_name=b'Summary of book', blank=True)),
                ('genre', models.CharField(max_length=500, verbose_name=b'Genre', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=b'Name of Store')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserToStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(default=b'rw', max_length=15, verbose_name=b'Kind of access granted to user.', choices=[(b'r', b'Read'), (b'w', b'Write'), (b'rw', b'Read-Write')])),
                ('store', models.ForeignKey(to='bookservices.Store')),
                ('user', models.ForeignKey(related_name='storerel', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='store',
            name='allowedUsers',
            field=models.ManyToManyField(related_name='store', through='bookservices.UserToStore', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventory',
            name='book',
            field=models.ForeignKey(to='bookservices.LibraryBook'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventory',
            name='store',
            field=models.ForeignKey(to='bookservices.Store'),
            preserve_default=True,
        ),
    ]
