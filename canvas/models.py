from django.db import models

ACTIVITIES = {
    1: 'NEW_USER',
    2: 'NEW_USER',
    3: 'NEW_USER',
    4: 'NEW_USER',
    5: 'NEW_USER',
}


class ActivityLogManager(models.Manager):
    pass


class ActivityLog(models.Model):
    objects = ActivityLogManager()
    