#!/usr/bin/python3.5

from ansible.module_utils.basic import *
import xmlrpc.client

def main():
    module = AnsibleModule(
            argument_spec = dict(
                url             = dict(required=True),
                username        = dict(aliases=['name'], required=True),
                password        = dict(required=True),
                first_name      = dict(required=False),
                last_name       = dict(required=False),
                user_url        = dict(required=False),
                display_name    = dict(required=False), 
                nickname        = dict(required=False),
                nice_name       = dict(required=False),
                bio             = dict(required=False),
            ),
        supports_check_mode=True
    )

    params = module.params
    server = xmlrpc.client.ServerProxy('%s/xmlrpc.php' % params['url'])

    existing_users = server.wp.getUsers(1, params['username'], params['password'])
    current_user = None
    for u in existing_users:
        if u['username'] == params['username']:
            current_user = u
            break

    details = {}
    skip_fields = ['username', 'name', 'password', 'url']
    mappings = {"user_url": "url"}
    for k, v in params.items():
        if k in skip_fields:
            continue
        if v:
            if k in mappings:
                k = mappings[k]
            details[k] = v

        is_changed=False
        for k, v in details.items():
            if current_user[k] != details[k]:
                current_user[k] = details[k]
                is_changed = True
            if is_changed and not module.check_mode:
                server.wp.editProfile(1, params['username'], params['password'], details)

        module.exit_json(changed=is_changed, user=dict(current_user))

if __name__ == '__main__':
    main()
