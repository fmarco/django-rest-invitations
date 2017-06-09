## django-rest-invitations

Rest customizable extension for [django-invitations](https://github.com/bee-keeper/django-invitations)


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

    Path. Serializer class for invitations (read)

*   `INVITATION_SERIALIZER_WRITE` (default=`rest_invitations.serializers.InvitationWriteSerializer`)

    Path. Serializer class for invitations (write)

*   `INVITATION_SERIALIZER_WRITE_BULK` (default=`rest_invitations.serializers.InvitationBulkWriteSerializer`)

    Path. Serializer class for invitations (bulk write)

*   `INVITATION_API_BASE_URL` (default=`invitations`)

    String. Base api url.

*   `INVITATION_SEND_URL` (default=`send`)

    String. Set up url on send endpoint

*   `INVITATION_CREATE_AND_SEND_URL` (default=`create-and-send`)

    String. Set up url on create_and_send endpoint

*   `INVITATION_SEND_MULTIPLE_URL` (default=`send-multiple`)

    String. Set up url on send_multiple endpoint


### APIs (examples with default values)

*   Invitations list

    /invitations/ (list, create)

    body request (create): email (string)

*   Invitation detail

    /invitations/(?P<pk>[^/.]+)/ (retrieve)

*   Invitation send

    /invitations/(?P<pk>[^/.]+)/send/ (post)

    body request: None

*   Invitation create and send

    invitations/create-and-send/ (post)

    body request: email (string)

*   Invitation multiple send

    invitations/send-multiple/ (post)

    body request: email: list of strings


### TODOS

* Tests
* ...


### Contributions

Feel free to contribute!
