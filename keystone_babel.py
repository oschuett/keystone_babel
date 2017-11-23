#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import flask
import requests

from keystoneauth1.extras._saml2 import V3Saml2Password
from keystoneauth1.identity.v3 import Token
from keystoneauth1 import session

app = flask.Flask(__name__)

OS_AUTH_URL = 'https://pollux.cscs.ch:13000/v3'
OS_IDENTITY_PROVIDER = 'cscskc'
OS_IDENTITY_PROVIDER_URL = 'https://kc.cscs.ch/auth/realms/cscs/protocol/saml/'
OS_PROTOCOL = 'mapped'
OS_INTERFACE = 'public'


# TODO implement / forward entire keystone API
# https://developer.openstack.org/api-ref/identity/v3/


#===============================================================================
@app.route('/v3/auth/tokens', methods=['POST'])
def tokens():

    # parse request
    body = flask.request.get_json()
    user = body['auth']['identity']['password']['user']
    username = user['name']
    password = user['password']

    # get unscoped token via SAML
    auth = V3Saml2Password(auth_url=OS_AUTH_URL,
                           identity_provider=OS_IDENTITY_PROVIDER,
                           protocol=OS_PROTOCOL,
                           identity_provider_url=OS_IDENTITY_PROVIDER_URL,
                           username=username,
                           password=password)
    sess = session.Session(auth=auth)
    unscoped_token = sess.get_token()

    # patch original body
    del(body['auth']['identity'])
    body['auth']['identity'] = {"methods": ["token"],
                                "token": {"id": unscoped_token}}

    # get scoped token
    r = requests.post(OS_AUTH_URL+'/auth/tokens', json=body)

    # TODO: maybe patch service catalog?

    # forward response
    return flask.Response(r.text, headers=dict(r.headers), status=r.status_code)

#===============================================================================
if __name__ == "__main__":
    app.run(port=5000, debug=True)

#EOF