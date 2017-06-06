from rest_framework import serializers
from invitations.utils import get_invitation_model

InvitationModel = get_invitation_model()


class InvitationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationModel
        fields = ('email', 'inviter')


class InvitationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationModel
        fields = '__all__'
