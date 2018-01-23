# -*- coding: utf-8 -*-
from bot.models import *
from products.models import *
from users.models import *
from orders.models import *
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
            print(request.data)
            sender_id, message = self.recive_message(data=request.data)
            if sender_id and message:
                self.make_response(sender_id, message)
            return Response(status=status.HTTP_201_CREATED)
        return HttpResponse(request.GET['hub.challenge'], content_type='text/plain')

    def make_response(self, sender_id, message):
        conversation, created = Conversation.objects.get_or_create(sender_id=sender_id, finished=False)
        if message == 'YES_JUICE' or message=='NEW_ORDER_PAYLOAD':
            elements = ProductCategory.objects.to_quick_reply(ProductCategory.objects.all())
            response = QuickReplyResponse(message='Que cosa?', elements=elements)
        elif message =='FINISH_ORDER_PAYLOAD':
            order_list = OrderList.objects.get(finished=False)
            order_list.finished = True
            order_list.save()
            response = SimpleTextMessage(message=order_list.resume)
        elif message == 'ORDER_LIST_PAYLOAD':
            try:
                order_list = OrderList.objects.get(finished=False)
                response = SimpleTextMessage(message=order_list.resume)
            except Exception as e:
                response = SimpleTextMessage(message='No hay listas abiertas')
        elif message == 'NO_JUICE':
            response = SimpleTextMessage(message='Cieza ctm')
        elif 'ADDON_CATEGORY_' in message:
            data = message.split('_')
            addon_category = data[2]
            product_order_id = data[3]
            addons = ProductAddon.objects.filter(addon_category=addon_category)
            elements = ProductAddon.objects.to_quick_reply(addons, product_order_id)
            response = QuickReplyResponse(message='Elige opcion', elements=elements)
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
        elif 'AMOUNT_' in message:
            data = message.split('_')
            amount = data[1]
            product_id = data[2]
            user , user_created = User.objects.get_or_create(facebook_id=sender_id)
            product = Product.objects.get(id=product_id)
            order_list, created = OrderList.objects.get_or_create(finished=False)
            order, order_created = order_list.order_details.get_or_create(user=user, order_list=order_list)
            product_order, product_order_created = order.orders_detail.get_or_create(product=product)
            product_order.amount = amount
            product_order.save()
            queryset = product.category.addon_categories.all()
            addon_categories = ProductAddonCategory.objects.to_quick_reply(queryset, product_order.id)
            response = QuickReplyResponse(message='Algun complemento?', elements=addon_categories)
        elif 'START' == message:
            response = InitialResponse()
            user, created = User.objects.get_or_create(facebook_id=sender_id)
            user.name = self.get_user_name(sender_id)
            user.save()
        elif 'NO_MORE_ADDON_' in message:
            product_order_id = message.split('_')[3]
            product_order = ProductOrder.objects.get(id=product_order_id)
            response = InitialResponse(message='Algo mas?')
        elif 'MORE_ADDON_' in message:
            product_order_id = message.split('_')[2]
            product_order = ProductOrder.objects.get(id=product_order_id)
            queryset = product_order.product.category.addon_categories.all()
            addon_categories = ProductAddonCategory.objects.to_quick_reply(queryset, product_order.id)
            response = QuickReplyResponse(message='Que otro complemento?', elements=addon_categories)
        elif 'ADDON_' in message:
            data = message.split('_')
            addon_id = data[1]
            # response = InitialResponse(message='Algo mas?')
            product_order_id = data[2]
            product_order = ProductOrder.objects.get(id=product_order_id)
            addon = ProductAddon.objects.get(id=addon_id)
            product_order.addons.add(addon)
            product_order.save()
            elements = ProductAddon.objects.more_options_reply(product_order_id)
            response = QuickReplyResponse(message='Otro complemento?', elements=elements)
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
        print(message)
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": message,
        })

        r = requests.post("https://graph.facebook.com/v2.11/me/messages",
                          params=params, headers=headers, data=data)

        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

    def get_user_name(self, id):
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.get('https://graph.facebook.com/v2.11/{0}'.format(id),
                          params=params, headers=headers)
        print(r)
        print(r.status_code)
        print(r.json())
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

        firstname = r.json().get('first_name', '')
        lastname = r.json().get('last_name', '')
        return '{0} {1}'.format(firstname, lastname)

    def log(self, message):  # simple wrapper for logging to stdout on heroku
        print(str(message))
