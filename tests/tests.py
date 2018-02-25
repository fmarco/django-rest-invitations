from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils import timezone
from invitations.utils import get_invitation_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
Invitation = get_invitation_model()


class TestInvitationAPI(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(TestInvitationAPI, cls).setUpClass()
        cls.user = User.objects.create_user(
            email='user@example.org', username='test_user', password='test'
        )

    def test_invitation_send(self):
        self.assertEqual(len(mail.outbox), 0)
        invitation = Invitation.create(email='invited@example.org')
        url = reverse('invitation-send', kwargs={'pk': invitation.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)
        self.client.login(username=self.user.username, password='test')
        url = reverse('invitation-send', kwargs={'pk': invitation.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_invitation_create_and_send(self):
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Invitation.objects.count(), 0)
        url = reverse('invitation-create-and-send')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Invitation.objects.count(), 0)
        self.client.login(username=self.user.username, password='test')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Invitation.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        data = {'email': 'invite@me.org'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_invitation_send_multiple(self):
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Invitation.objects.count(), 0)
        url = reverse('invitation-send-multiple')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Invitation.objects.count(), 0)
        self.client.login(username=self.user.username, password='test')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Invitation.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        data = {'email': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Invitation.objects.count(), 0)
        data = {'email': ['invite@me.org', 'invite2@alt.com']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(Invitation.objects.count(), 2)
        data = {'email': ['invite@me.org', 'invite2@alt.com']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(Invitation.objects.count(), 2)
        data = {'email': ['invite@me.org']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(Invitation.objects.count(), 2)
        data = {'email': ['invite2@alt.com']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(Invitation.objects.count(), 2)

    def test_invitation_accept(self):
        invitation = Invitation.create(
            email='invited@email.org',
            inviter=self.user
        )
        invitation_pk = invitation.pk
        invitation.sent = timezone.now()
        invitation.save()
        url = reverse('invitations:accept-invite', kwargs={'key': 'something'})
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertFalse(invitation.accepted)
        url = reverse(
            'invitations:accept-invite',
            kwargs={'key': invitation.key}
        )
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invitation = Invitation.objects.get(pk=invitation_pk)
        self.assertTrue(invitation.accepted)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_410_GONE)

    def tearDown(self):
        self.client.logout()
