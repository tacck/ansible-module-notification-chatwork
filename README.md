# ansible-module-notification-chatwork

## DOCUMENTATION
```
module: chatwork
version_added: "0.1"
short_description: Send a message to ChatWork.
description:
   - Send a message to a ChatWork room.
options:
  token:
    description:
      - API token.
    required: true
  room:
    description:
      - ID of the room.
    required: true
  msg:
    description:
      - The message body.
    required: true
  title:
    description:
      - The message title.
    required: false
    default: None
```

## EXAMPLES
```
- chatwork:
    token: API_TOKEN
    room: ROOM_ID_NUMBER
    title: Notification from Ansible
    msg: Ansible task finished
```