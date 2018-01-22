# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model, JSONField
from django.db import models


class Message(TimeStampedModel, Model):

    text = models.CharField(
        max_length=5000,
        help_text='user message',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS


class Conversation(TimeStampedModel):

    context = JSONField()
    sender_id = models.CharField(
        max_length=5000,
    )

    grade = models.CharField(
        max_length=100,
        null=True,
    )

    confidence_person = models.CharField(
        max_length=100,
        null=True,
    )

    grade_section = models.CharField(
        max_length=100,
        null=True,
    )

    grade_level = models.CharField(
        max_length=100,
        null=True,
    )

    problem_location = models.CharField(
        max_length=100,
        null=True,
    )

    genre = models.CharField(
        max_length=10,
        null=True,
    )

    violence_type = models.CharField(
        max_length=100,
        null=True,
    )

    topics = JSONField()

    district = models.CharField(
        max_length=100,
        null=True,
    )

    sentiment = models.CharField(
        max_length=100,
        null=True,
    )

    sentiment_value = models.DecimalField(
        max_digits=19,
        decimal_places=10,
        null=True,
    )

    detect_sentiment = models.NullBooleanField()

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class BaseResponse():

    def __init__(self, message='', elements=[]):
        self.elements = elements
        self.message = message

    def render(self):
        pass

class PostbackButtonsResponse(BaseResponse):
    template_type = 'button'
    """docstring for ButtonsResponse"""

    def render(self):
        return {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': self.template_type,
                    'text': self.message,
                    'buttons': [self.map_buttons(button) for button in buttons],
                }
            }
        }

    def map_buttons(self, element):
        return {
            'type': 'postback',
            'title': element.get('title', ''),
            'payload': element.get('payload', ''),
        }

class SimpleTextMessage(BaseResponse):
    """docstring for SimpleTextMessage"""
    def __init__(self, message=''):
        self.message = message

    def render(self):
        return {
            'text': self.message
        }

class QuickReplyResponse(BaseResponse):
    """docstring for QuickReplyResponse"""
    content_type = 'text'

    def render(self):
        return {
            'text': self.message,
            'quick_replies': [self.map_buttons(element) for element in elements],
        }

    def map_buttons(self, element):
        return {
            'content_type': self.content_type,
            'title': element.get('title', ''),
            'payload': element.get('payload', ''),
        }


class InitialResponse(BaseResponse):
    """docstring for InitialResponse"""
    def __init__(self):
        self.message = 'Jugos?'
        self.elements = [
            {
                'title': 'Si',
                'payload': 'YES_JUICE',
            },
            {
                'title': 'No',
                'payload': 'NO_JUICE',
            },
        ]

class ErrorResponse(SimpleTextMessage):
    """docstring for ErrorResponse"""
    def __init__(self):
        self.message = 'No entendi, Igor ctm'







