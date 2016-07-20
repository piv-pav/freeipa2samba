#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import ldap
from sh import pdbedit

config = { 
        "ldap_host":    "ldap://{your_ldap_server}/",
        "ldap_user":    "uid=search,cn=users,cn=accounts,dc=switch,dc=internal",
        "ldap_pass":    "{user_password}",
        "base_dn":      "cn=users,cn=accounts,dc=switch,dc=internal",
        "blocked_users": ['admin', 'search'],
        }

# Connceting to the IPA LDAP
try:
    ipa_ldap = ldap.initialize(config['ldap_host'])
    ipa_ldap.protocol_version = ldap.VERSION3
    ipa_ldap.simple_bind(config['ldap_user'], config['ldap_pass'])
except ldap.LDAPError as e:
    print(e)
    exit(1)

# Searching for users
try:
    attributes = ['uid', 'ipaNTHash']
    ldap_result_id = ipa_ldap.search(config['base_dn'], ldap.SCOPE_SUBTREE, "(uid=*)", attributes)
    result_type, result_data = ipa_ldap.result(ldap_result_id, 10000)

    if result_data == []: 
        print("LDAP search has returned nothing! NOTHING!!! AAAA!!!!!")
        exit(3)
    else:
        users = result_data
except ldap.LDAPError as e:
    print(e)
    exit(2)

for uid, user in users:
    login = user['uid'][0]
    # Check if the user has NTLM Hash and not blacklisted
    if 'ipaNTHash' in user and not login in config['blocked_users']:
        # Converting hash to samba-readable format
        nt_hash = binascii.b2a_hex(user['ipaNTHash'][0]).upper()
    else:
        continue

    # Checking if user already in the DB
    try:
        pdbedit('-L', '-u', login)
    except:
        # User doesn't exist in the database, creating user
        # Password here doesn't really matter, because it will be wiped by NT Hash
        pdbedit("-a", "-u", login, "-t", _in="Doesn't Matter\nDoesn't Matter\n")

    # Updating user's hash
    pdbedit('-u', login, '--set-nt-hash', nt_hash)
