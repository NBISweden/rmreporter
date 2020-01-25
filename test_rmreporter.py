#!/usr/bin/env python8

import rmreporter
import unittest.mock
import io
import sys


@unittest.mock.patch('builtins.open')
@unittest.mock.patch('os.path.exists')
@unittest.mock.patch('builtins.input')
@unittest.mock.patch('getpass.getpass')
def test_credentials(gp, i, ope, bo):
    ope.return_value = False
    i.return_value = 'svar1'
    gp.return_value = 'passv1'

    # Nothing on command line
    a = rmreporter.get_credentials(None)

    assert a['username'] == 'svar1'
    assert a['url'] == 'svar1'
    assert a['password'] == 'passv1'

    # With options
    opt = unittest.mock
    opt.username = 'svar2'
    opt.url = 'svar3'
    opt.password = 'passv2'

    b = rmreporter.get_credentials(opt)

    assert b['username'] == 'svar2'
    assert b['url'] == 'svar3'
    assert b['password'] == 'passv2'

    # And from config file
    ope.return_value = True
    bo.return_value = io.StringIO("""[credentials]
username = svar3
url = svar4
password = passv3
""")
    c = rmreporter.get_credentials(None)

    assert c['username'] == 'svar3'
    assert c['url'] == 'svar4'
    assert c['password'] == 'passv3'


def test_options():
    sys.argv = ['', 'så', 'lunka', 'vi']
    o, a = rmreporter.get_options()
    assert a == ['så', 'lunka', 'vi']

    assert not o.username
    assert not o.url
    assert not o.password

    sys.argv = ['', '--url=så', '--password=småningom', '-u', 'mot', 'bacchi']
    o, a = rmreporter.get_options()
    assert a == ['bacchi']

    assert o.username == 'mot'
    assert o.url == 'så'
    assert o.password == 'småningom'
