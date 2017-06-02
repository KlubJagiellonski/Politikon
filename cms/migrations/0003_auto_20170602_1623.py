# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0002_auto_20170521_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.ImageField(upload_to=b'images')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'gallery image',
                'verbose_name_plural': 'gallery images',
            },
        ),
        migrations.AlterField(
            model_name='extracontent',
            name='content',
            field=models.TextField(verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='extracontent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='extracontent',
            name='lang',
            field=models.CharField(default=b'pl', max_length=2, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='extracontent',
            name='tag_code',
            field=models.SlugField(verbose_name='tag code'),
        ),
        migrations.AlterField(
            model_name='extracontent',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='edition date'),
        ),
        migrations.AlterField(
            model_name='extracontent',
            name='user_profile',
            field=models.ForeignKey(related_query_name=b'extra_contents', related_name='extra_content', verbose_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.TextField(verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='page',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='is published'),
        ),
        migrations.AlterField(
            model_name='page',
            name='lang',
            field=models.CharField(default=b'pl', max_length=2, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug url'),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255, verbose_name='news title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='edition date'),
        ),
        migrations.AlterField(
            model_name='page',
            name='user_profile',
            field=models.ForeignKey(related_query_name=b'pages', related_name='page', verbose_name='author', to=settings.AUTH_USER_MODEL),
        ),
    ]
