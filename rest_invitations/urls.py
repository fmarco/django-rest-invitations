from django.conf.urls import include, url
from rest_framework import routers

from .views import InvitationViewSet, accept_invitation

router = routers.SimpleRouter()
router.register(r'invitations', InvitationViewSet)

invitations_patterns = (
    [
        url(r'^accept-invite/(?P<key>\w+)/?$', accept_invitation,
        name='accept-invite'),
    ],
    'invitations'
)

urlpatterns = router.urls + [
    url(r'^', include(invitations_patterns)),
]
