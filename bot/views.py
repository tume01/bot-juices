# -*- coding: utf-8 -*-
from bot.models import *
from products.models import *
from bot.serializers import ConversationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.http import HttpResponse
from rest_framework import status
from django.conf import settings
from django.db.models import Count
import json
import requests


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @list_route(methods=['post', 'get'])
    def webhook(self, request):
        if request.method == 'POST':
            sender_id, message = self.recive_message(data=request.data)
            if sender_id and message:
                self.make_response(sender_id, message)
            return Response(status=status.HTTP_201_CREATED)
        return HttpResponse(request.GET['hub.challenge'], content_type='text/plain')

    def make_response(self, sender_id, message):
        print(message)
        conversation, created = Conversation.objects.get_or_create(sender_id=sender_id, finished=False)
        if created:
            self.send_message(sender_id, InitialResponse())
        else:
            if message == 'YES_JUICE' or message=='NEW_ORDER_PAYLOAD':
                elements = ProductCategory.objects.to_quick_reply(ProductCategory.objects.all())
                response = QuickReplyResponse(message='Que cosa?', elements=elements)
            elif message == 'NO_JUICE':
                response = SimpleTextMessage(message='Cieza ctm')
            elif 'CATEGORY_' in message:
                category_id = message.split('_')[1]
                category = ProductCategory.objects.get(id=category_id)
                elements = Product.objects.to_quick_reply(Product.objects.filter(category=category))
                response = PostbackButtonsResponse(message='Que {0}?'.format(category.description), elements=elements)
            elif 'PRODUCT_' in message:
                product_id = message.split('_')[1]
                product = Product.objects.get(id=product_id)
                elements = Product.objects.to_amount_reply(product)
                response = QuickReplyResponse(message='Cuantos?', elements=elements)
            else:
                response = ErrorResponse()
            self.send_message(sender_id, response)

    def recive_message(self, data={}):
        if data.get('object', None) == "page":
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event.get('sender', {}).get('id', None)
                    if messaging_event.get('message', None):
                        message = messaging_event.get('message', {})
                        message_text = message.get('text', '')
                        if message.get('quick_reply', None):
                            message_text = message.get('quick_reply').get('payload')
                        return sender_id, message_text
                    if messaging_event.get('postback', None):
                        postback = messaging_event.get('postback')
                        message_text = postback.get('payload')
                        return sender_id, message_text
        return None, None

    def send_message(self, recipient_id, response):
        params = {
            "access_token": settings.BOT_APP_TOKEN
        }

        headers = {
            "Content-Type": "application/json"
        }

        message = response.render()

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": message,
        })

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params=params, headers=headers, data=data)

        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

    def log(self, message):  # simple wrapper for logging to stdout on heroku
        print(str(message))
