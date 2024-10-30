import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message
from django.contrib.auth.models import User
from project.models import Project

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extraer project_id y recipient_id de la URL de la ruta
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']

        # Definir el room_group_name basado en project_id y recipient_id
        self.room_group_name = f"chat_{self.project_id}_{self.recipient_id}"

        # Unir al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        recipient_id = data['recipient_id']
        project_id = data['project_id']

        # Guardar el mensaje en la base de datos
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        recipient = await sync_to_async(User.objects.get)(id=recipient_id)
        project = await sync_to_async(Project.objects.get)(id=project_id)

        await sync_to_async(Message.objects.create)(
            sender=sender,
            recipient=recipient,
            project=project,
            content=message
        )

        # Enviar el mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': sender.username
            }
        )

    # Método que maneja el mensaje recibido y lo envía a WebSocket
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))
