# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_code', models.SlugField(verbose_name='Tag code')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Edition date')),
                ('content', models.TextField(verbose_name='Content')),
                ('lang', models.CharField(default=b'pl', max_length=2, verbose_name='Language')),
                ('user_profile', models.ForeignKey(related_query_name=b'extra_contents', related_name='extra_content', verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('title', models.CharField(max_length=255, verbose_name='News title')),
                ('slug', models.SlugField(verbose_name='Slug url')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Edition date')),
                ('content', models.TextField(verbose_name='Content')),
                ('lang', models.CharField(default=b'pl', max_length=2, verbose_name='Language')),
                ('user_profile', models.ForeignKey(related_query_name=b'pages', related_name='page', verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
