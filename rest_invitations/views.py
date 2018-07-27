from django.contrib import messages
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings as invitations_settings
from invitations.signals import invite_accepted
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import (api_view, detail_route, list_route,
                                       permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .app_settings import (CREATE_AND_SEND_URL, SEND_MULTIPLE_URL, SEND_URL,
                           InvitationBulkWriteSerializer, InvitationModel,
                           InvitationReadSerializer, InvitationWriteSerializer)


class InvitationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = InvitationModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InvitationReadSerializer
        elif self.action == 'send_multiple':
            return InvitationBulkWriteSerializer
        return InvitationWriteSerializer

    def _prepare_and_send(self, invitation, request):
        invitation.inviter = request.user
        invitation.save()
        invitation.send_invitation(request)

    @detail_route(
        methods=['post'], permission_classes=[IsAuthenticated],
        url_path=SEND_URL
    )
    def send(self, request, pk=None):
        invitation = self.get_object()
        self._prepare_and_send(invitation, request)
        content = {'detail': 'Invite sent'}
        return Response(content, status=status.HTTP_200_OK)

    @list_route(
        methods=['post'], permission_classes=[IsAuthenticated],
        url_path=CREATE_AND_SEND_URL
    )
    def create_and_send(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        invitation = InvitationModel.create(email=email, inviter=request.user)
        self._prepare_and_send(invitation, request)
        content = {'detail': 'Invite sent'}
        return Response(content, status=status.HTTP_200_OK)

    @list_route(
        methods=['post'], permission_classes=[IsAuthenticated],
        url_path=SEND_MULTIPLE_URL
    )
    def send_multiple(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inviter = request.user
        for email in serializer.data['email']:
            invitation = InvitationModel.create(email=email, inviter=inviter)
            self._prepare_and_send(invitation, request)
        content = {'detail': 'Invite(s) sent'}
        return Response(content, status=status.HTTP_200_OK)


@api_view(('POST', 'GET'))
@permission_classes((AllowAny,))
def accept_invitation(request, key):
    def get_object():
        try:
            return InvitationModel.objects.get(key=key.lower())
        except InvitationModel.DoesNotExist:
            return None

    invitation = get_object()

    login_data = {
        'LOGIN_REDIRECT': invitations_settings.LOGIN_REDIRECT
    }
    signup_data = {
        'SIGNUP_REDIRECT': invitations_settings.SIGNUP_REDIRECT
    }

    if invitations_settings.GONE_ON_ACCEPT_ERROR and \
        (not invitation or
         (invitation and (invitation.accepted or
                          invitation.key_expired()))):
        return Response(status=status.HTTP_410_GONE)

    if not invitation:
        get_invitations_adapter().add_message(
            request,
            messages.ERROR,
            'invitations/messages/invite_invalid.txt'
        )
        return Response(login_data, status=status.HTTP_200_OK)

    if invitation.accepted:
        get_invitations_adapter().add_message(
            request,
            messages.ERROR,
            'invitations/messages/invite_already_accepted.txt',
            {
                'email': invitation.email
            }
        )
        return Response(login_data, status=status.HTTP_200_OK)

    if invitation.key_expired():
        get_invitations_adapter().add_message(
            request,
            messages.ERROR,
            'invitations/messages/invite_expired.txt',
            {
                'email': invitation.email
            }
        )
        return Response(signup_data, status=status.HTTP_200_OK)

    if not invitations_settings.ACCEPT_INVITE_AFTER_SIGNUP:
        invitation.accepted = True
        invitation.save()
        invite_accepted.send(sender=None, email=invitation.email)
        get_invitations_adapter().add_message(
            request,
            messages.SUCCESS,
            'invitations/messages/invite_accepted.txt',
            {
                'email': invitation.email
            }
        )
        signup_data.update(
            {
                'account_verified_email': invitation.email
            }
        )
    return Response(
        signup_data,
        status=status.HTTP_200_OK
    )
