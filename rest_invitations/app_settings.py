from django.conf import settings
from invitations.utils import get_invitation_model

from .serializers import InvitationReadSerializer as DefaultInvitationReadSerializer
from .serializers import InvitationWriteSerializer as DefaultInvitationWriteSerializer


InvitationReadSerializer = getattr(settings, 'INVITATION_SERIALIZER_READ', DefaultInvitationReadSerializer)
InvitationWriteSerializer = getattr(settings, 'INVITATION_SERIALIZER_WRITE', DefaultInvitationWriteSerializer)


InvitationModel = get_invitation_model()
