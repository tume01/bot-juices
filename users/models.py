# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model
from django.db import models

class UserManager(models.Manager):
    pass

class User(TimeStampedModel):

    facebook_id = models.CharField(
        max_length=100,
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    objects = UserManager()

    def __str__(self):
        return self.name if self.name else self.facebook_id

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS