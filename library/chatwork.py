#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Kihara, Takuya <gray.tk@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
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

requirements: [ ]
author: "Kihara, Takuya (@tacck)"
'''

EXAMPLES = '''
- chatwork:
    token: API_TOKEN
    room: ROOM_ID_NUMBER
    title: Notification from Ansible
    msg: Ansible task finished
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils.six.moves.urllib.request import pathname2url
from ansible.module_utils.urls import fetch_url

DEFAULT_URI = "https://api.chatwork.com/v2"
ROOM_POST_URI = "/rooms/{room_id}/messages"

def send_msg(module, token, room, msg, title):

    # Set URL
    POST_URL = DEFAULT_URI + ROOM_POST_URI
    url = POST_URL.replace('{room_id}', pathname2url(room))

    # Set Headers
    headers = {'X-ChatWorkToken': token}

    # Set Body
    data = "body=" + "[info]"
    if title is not None:
        data += "[title]" + title + "[/title]"
    data += msg + "[/info]"

    response, info = fetch_url(module, url, data=data, headers=headers, method='POST')

    if info['status'] == 200:
        return response.read()
    else:
        module.fail_json(msg="failed: return status=%s" % str(info['status']))

def main():
    module = AnsibleModule(
        argument_spec = dict(
            token   = dict(required=True, no_log=True),
            room    = dict(required=True, type='int'),
            msg     = dict(required=True),
            title   = dict(required=False, default=None),
        ),
        supports_check_mode=True
    )

    token   = module.params["token"]
    room    = str(module.params["room"])
    msg     = module.params["msg"]
    title   = module.params["title"]

    try:
        send_msg(module, token, room, msg, title)
    except Exception:
        e = get_exception()
        module.fail_json(msg="unable to send msg: %s" % e)

    changed = True
    module.exit_json(changed=changed, room=room, msg=msg)

if __name__ == '__main__':
    main()
