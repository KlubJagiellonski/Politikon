# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160202_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=image_cropping.fields.ImageCropField(upload_to=b'events_big', null=True, verbose_name='obrazek 1250x510'),
        ),
        migrations.AlterField(
            model_name='event',
            name='big_image',
            field=image_cropping.fields.ImageRatioField(b'image', '1250x510', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big image'),
        ),
        migrations.AlterField(
            model_name='event',
            name='small_image',
            field=image_cropping.fields.ImageRatioField(b'image', '340x250', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small image'),
        ),
    ]
