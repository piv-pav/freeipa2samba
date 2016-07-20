# freeipa2samba

## Description

Script to populate users from FreeIPA to Samba4 passwd.tdb database.

Unfortunately connecting Samba4 to the IPA server without creating AD and trusts
is a pain in the arse, that's the only reason why this script has been written.


## Requirements

1. Samba 4.4.3 + (Not available in most repos at the time of writing.)
2. FreeIPA 4 +
3. FreeIPA ad-trust module


## Config

Example minimal samba config:

```
[global]
        log file = /var/log/samba/log.%m
        security = user

[homes]
        browsable = no
        writable = yes

[shared]
        path = /mnt/xxx_videos/
        writable = no
        browsable=yes
```

The script relies on the pdbedit binary, if you have installed Samba from source 
the path will likely be incorrect. You can update it as such:

```
from sh import pdbedit
```
to 
```
import sh
pdbedit = sh.Command("/usr/local/samba/bin/pdbedit")
```
Script also uses python-sh package, so it's on you to satisfy dependencies =)


## Notes/Security Concerns

1. NT Hash's are as good as passwords. You MUST secure your passdb.tdb file so that it's readable by root and samba only.
2. If you install freeipa-adtrust after user creation, users will have to reset their passwords in order for the NtHash to be generated.
