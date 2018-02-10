from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from invitations.adapters import get_invitations_adapter
from invitations.exceptions import AlreadyInvited, AlreadyAccepted, UserRegisteredEmail
from invitations.utils import get_invitation_model

InvitationModel = get_invitation_model()


errors = {
    "already_invited": _("This e-mail address has already been"
                         " invited."),
    "already_accepted": _("This e-mail address has already"
                          " accepted an invite."),
    "email_in_use": _("An active user is using this e-mail address"),
}


class EmailListField(serializers.ListField):
    """Email list field."""

    child = serializers.EmailField()


class InvitationWriteSerializer(serializers.ModelSerializer):
    """Invitation write serializer."""

    class Meta(object):
        """Options."""

        model = InvitationModel
        fields = ('email',)

    def _validate_invitation(self, email):
        """Validate invitation.

        :param email:
        :return:
        """
        if InvitationModel.objects.all_valid().filter(email__iexact=email,
                                                      accepted=False):
            raise AlreadyInvited
        elif InvitationModel.objects.filter(email__iexact=email,
                                            accepted=True):
            raise AlreadyAccepted
        elif get_user_model().objects.filter(email__iexact=email):
            raise UserRegisteredEmail
        else:
            return True

    def validate_email(self, email):
        """Validate email.

        :param email:
        :return:
        """
        email = get_invitations_adapter().clean_email(email)

        try:
            self._validate_invitation(email)
        except AlreadyInvited:
            raise serializers.ValidationError(errors["already_invited"])
        except AlreadyAccepted:
            raise serializers.ValidationError(errors["already_accepted"])
        except UserRegisteredEmail:
            raise serializers.ValidationError(errors["email_in_use"])
        return email

    def create(self, validate_data):
        """Create.

        :param validate_data:
        :return:
        """
        return InvitationModel.create(**validate_data)


class InvitationReadSerializer(serializers.ModelSerializer):
    """Invitation read serializer."""

    class Meta(object):
        """Options."""

        model = InvitationModel
        fields = '__all__'


class InvitationBulkWriteSerializer(InvitationWriteSerializer):
    """Invitation bulk serializer."""

    email = EmailListField()

    class Meta(InvitationWriteSerializer.Meta):
        """Options."""

        model = InvitationModel
        fields = InvitationWriteSerializer.Meta.fields

    def validate_email(self, email_list):
        """Validate email.

        :param email_list:
        :return:
        """
        if len(email_list) == 0:
            raise serializers.ValidationError(_('You must add one or more email addresses'))
        for email in email_list:
            email = get_invitations_adapter().clean_email(email)
            try:
                self._validate_invitation(email)
            except AlreadyInvited:
                raise serializers.ValidationError(errors["already_invited"])
            except AlreadyAccepted:
                raise serializers.ValidationError(errors["already_accepted"])
            except UserRegisteredEmail:
                raise serializers.ValidationError(errors["email_in_use"])

        return email_list
