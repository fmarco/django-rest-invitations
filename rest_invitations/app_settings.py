from django.conf import settings
from invitations.utils import get_invitation_model

from .serializers import InvitationReadSerializer as DefaultInvitationReadSerializer
from .serializers import InvitationWriteSerializer as DefaultInvitationWriteSerializer
from .serializers import InvitationBulkWriteSerializer as DefaultInvitationBulkWriteSerializer


InvitationReadSerializer = getattr(settings, 'INVITATION_SERIALIZER_READ', DefaultInvitationReadSerializer)
InvitationWriteSerializer = getattr(settings, 'INVITATION_SERIALIZER_WRITE', DefaultInvitationWriteSerializer)
InvitationBulkWriteSerializer = getattr(settings, 'INVITATION_SERIALIZER_WRITE_BULK', DefaultInvitationBulkWriteSerializer)


InvitationModel = get_invitation_model()
