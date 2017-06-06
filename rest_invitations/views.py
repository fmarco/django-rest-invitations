from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, detail_route, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response 

from invitations.app_settings import app_settings as invitation_settings
from invitations.adapters import get_invitations_adapter

from .app_settings import InvitationModel, InvitationReadSerializer, InvitationWriteSerializer


class InvitationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = InvitationModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrive']:
            return InvitationReadSerializer
        return InvitationWriteSerializer

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def send(self, request, pk=None):
        self.object = invitation = self.get_object()
        invitation.inviter = self.request.user
        invitation.save()
        invitation.send_invitation(self.request)
        content = {'detail': 'Invite sent'}
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
    # TODO...
