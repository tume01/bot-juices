# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model, JSONField
from django.db import models


class Conversation(TimeStampedModel):

    sender_id = models.CharField(
        max_length=5000,
    )

    finished = models.BooleanField(default=False)

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
                    'buttons': [self.map_buttons(button) for button in self.elements],
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
            'quick_replies': [self.map_buttons(element) for element in self.elements],
        }

    def map_buttons(self, element):
        return {
            'content_type': self.content_type,
            'title': element.get('title', ''),
            'payload': element.get('payload', ''),
        }


class InitialResponse(QuickReplyResponse):
    """docstring for InitialResponse"""
    def __init__(self, message='Jugos?'):
        self.message = message
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

class MoreProductsResponse(QuickReplyResponse):

    def __init__(self):
        self.message = 'Algo mas?'
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





