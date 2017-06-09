from django.conf import settings
from invitations.utils import get_invitation_model

from .serializers import \
    InvitationBulkWriteSerializer as DefaultInvitationBulkWriteSerializer
from .serializers import \
    InvitationReadSerializer as DefaultInvitationReadSerializer
from .serializers import \
    InvitationWriteSerializer as DefaultInvitationWriteSerializer
from .utils import import_callable

# Serializers
InvitationReadSerializer = import_callable(
    getattr(
        settings,
        'INVITATION_SERIALIZER_READ',
        DefaultInvitationReadSerializer
    )
)
InvitationWriteSerializer = import_callable(
    getattr(
        settings,
        'INVITATION_SERIALIZER_WRITE',
        DefaultInvitationWriteSerializer
    )
)
InvitationBulkWriteSerializer = import_callable(
    getattr(
        settings,
        'INVITATION_SERIALIZER_WRITE_BULK',
        DefaultInvitationBulkWriteSerializer
        )
)

# Urls
API_BASE_URL = getattr(
    settings, 'INVITATION_API_BASE_URL', 'invitations'
)
ACCEPT_INVITE_URL = getattr(
    settings, 'INVITATION_ACCEPT_INVITE_URL', 'accept-invite'
)
SEND_URL = getattr(
    settings, 'INVITATION_SEND_URL', 'send'
)
CREATE_AND_SEND_URL = getattr(
    settings, 'INVITATION_CREATE_AND_SEND_URL', 'create-and-send'
)
SEND_MULTIPLE_URL = getattr(
    settings, 'INVITATION_SEND_MULTIPLE_URL', 'send-multiple'
)

# Get Invitation model
InvitationModel = get_invitation_model()
