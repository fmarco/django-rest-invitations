## django-rest-invitations

Rest extension for [django-invitations](https://github.com/bee-keeper/django-invitations)


### Requirements

Make a proper setup for django-invitations.


### Installation

```
# Add to settings.py, INSTALLED_APPS
'rest_framework',
'invitations',
'rest_invitations'

# Append to urls.py
url(r'^', include('rest_invitations.urls'))
```

### Configuration

*   `INVITATION_SERIALIZER_READ` (default=`rest_invitations.serializers.InvitationReadSerializer`)

    Serializer class for invitations (read)

*   `INVITATION_SERIALIZER_WRITE` (default=`rest_invitations.serializers.InvitationWriteSerializer`)

    Serializer class for invitations (write)

*   `INVITATION_SERIALIZER_WRITE_BULK` (default=`rest_invitations.serializers.InvitationBulkWriteSerializer`)

    Serializer class for invitations (bulk write)


### TODOS

* Tests
* ...

Feel free to contribute!