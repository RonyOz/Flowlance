from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from project.models import Project, ProjectMember
from profile.models import FreelancerProfile, CompanyProfile, ProfileConfiguration
from chat.models import ChatRoom, Message
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatConsumer
from asgiref.testing import ApplicationCommunicator
import json

class ChatModelsTestCase(TestCase):
    def setUp(self):
        # Crear usuarios y proyecto para las pruebas
        self.profile_config, _ = ProfileConfiguration.objects.get_or_create()
        self.profile_config.notification_when_profile_visited = False
        self.profile_config.save()
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.company_profile = CompanyProfile.objects.create(user=self.user1, company_name='Test Company', nit='1234567890',profileconfiguration = self.profile_config)
        self.freelancer_profile = FreelancerProfile.objects.create(user=self.user2, identification='12345678', phone='123456789', profileconfiguration = self.profile_config)

        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project description.",
            requirements="Test requirements for the project.",
            budget=10000.00,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            client=self.user1,
            is_deleted=False
        )

    def test_chat_room_creation(self):
        # Crear una sala de chat
        room = ChatRoom.objects.create(project=self.project, name="room1")
        self.assertEqual(room.project, self.project)
        self.assertEqual(room.name, "room1")

    def test_message_creation(self):
        # Crear un mensaje y verificar que se guarda correctamente
        message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            project=self.project,
            content="Hello"
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.recipient, self.user2)
        self.assertEqual(message.content, "Hello")

    def test_soft_delete(self):
        # Verificar que el soft delete funcione
        message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            project=self.project,
            content="To be deleted"
        )
        message.hidden_for_sender = True
        message.hidden_for_recipient = True
        message.save()

        # Verificar que los flags de soft delete están establecidos correctamente
        self.assertTrue(message.hidden_for_sender)
        self.assertTrue(message.hidden_for_recipient)



class ChatViewsTestCase(TestCase):
    def setUp(self):
        self.profile_config, _ = ProfileConfiguration.objects.get_or_create()
        self.profile_config.notification_when_profile_visited = False
        self.profile_config.save()
        # Configuración de datos de prueba
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.company_profile = CompanyProfile.objects.create(user=self.user1, company_name='Test Company', nit='1234567890',profileconfiguration = self.profile_config)
        self.freelancer_profile = FreelancerProfile.objects.create(user=self.user2, identification='12345678', phone='123456789', profileconfiguration = self.profile_config)

        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project description.",
            requirements="Test requirements for the project.",
            budget=10000.00,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            client=self.user1,
            is_deleted=False
        )

        self.member1 = ProjectMember.objects.create(user=self.user1, project=self.project)
        self.member2 = ProjectMember.objects.create(user=self.user2, project=self.project)
        self.client.login(username="user1", password="pass")

    def test_chat_room_view(self):
        url = reverse("chat_room", args=[self.project.id, self.member2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chat con user2")

    def test_soft_delete_chat(self):
        # Crear un mensaje y luego eliminarlo para un usuario
        message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            project=self.project,
            content="Hello"
        )
        url = reverse("soft_delete_chat", args=[self.project.id, self.member2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # Recargar el mensaje y verificar que está oculto para el usuario
        message.refresh_from_db()
        self.assertTrue(message.hidden_for_sender)
