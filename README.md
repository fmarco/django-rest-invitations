## django-rest-invitations


[![Build Status](https://travis-ci.org/fmarco/django-rest-invitations.svg?branch=master)](https://travis-ci.org/fmarco/django-rest-invitations)

[![Coverage Status](https://coveralls.io/repos/fmarco/django-rest-invitations/badge.svg?branch=master&service=github)](https://coveralls.io/github/fmarco/django-rest-invitations?branch=master)

Rest customizable extension for [django-invitations](https://github.com/bee-keeper/django-invitations)

Supported Python versions:

* 3.5
* 3.6
* 3.7
* 3.8

Supported Django versions:

* Django 1.11
* Django 2.0
* Django 3.0

Supported DRF versions:

* at least DRF 3.10 or greater

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

*   `INVITATION_ACCEPT_INVITE_URL` (default=`accept-invite`)

    String. Set up url for accept_invitation endpoint


### APIs (examples with default values)

*   `Invitations list`

    - /invitations/ (list, create)

    body request (create): email (string)

*   `Invitation detail`

    - /invitations/`<pk>`/ (retrieve, destroy)

*   `Invitation send`

    - /invitations/`<pk>`/send/ (post)

    body request: None

*   `Invitation create and send`

    - /invitations/create-and-send/ (post)

    body request: email (string)

*   `Invitation multiple send`

    - /invitations/send-multiple/ (post)

    body request: email: list of strings

*   `Accept invitation`

    - /invitations/accept-invite/`<key>`/ (get)



### Contributions

Feel free to contribute!
