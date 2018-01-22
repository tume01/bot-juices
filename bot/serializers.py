# -*- coding: utf-8 -*-
from bot.models import Conversation
from rest_framework import serializers


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = (
            'id',
        )
