import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Booking, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        print("WebSocket trying to connect with user:", self.scope['user'])
        self.user = self.scope['user']

        # Access check: only customer or partner
        if not await self.check_booking_access(self.booking_id, self.user):
            await self.close()
            return

        self.room_group_name = f'chat_{self.booking_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        if not message:
            return

        await self.save_message(self.booking_id, self.user, message)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))

    @database_sync_to_async
    def check_booking_access(self, booking_id, user):
        try:
            booking = Booking.objects.get(id=booking_id)
            return user == booking.customer or user == booking.partner
        except Booking.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, booking_id, user, message):
        booking = Booking.objects.get(id=booking_id)
        return ChatMessage.objects.create(booking=booking, sender=user, message=message)
