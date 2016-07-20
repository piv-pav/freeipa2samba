# freeipa2samba
Script to populate users from FreeIPA to Samba4 passwd.tdb database.

Unfortunatellty connecting Samba4 to the IPA server without creating AD and trusts
is pain in the arse, that's the only reason why this script has been written.
To make it work you should have Samba 4.4+ and FreeIPA with ad-trust installed.
Samba before v.4.4 has no option to update NT Hash in the database, 
so don't even bother with earlier versions.

Your simple samba config should be like
```
[global]
        kerberos method = dedicated keytab
        log file = /var/log/samba/log.%m
        security = user

[homes]
        browsable = no
        writable = yes

[shared]
        path = /mnt/xxx_videos/
        writable = no
        browsable=yes
        write list = @admins
```
Of course you have to issue kerberos keytab for your samba server cifs/yoursambaserver.your.domain.com and put it next to smb.conf

In some cases (well most cases), you will have to compile Samba 4.4 from scratch and it's recomended to use PREFIX=/usr/local for that.
In that case this script won't work, due to it relays on your PATH environment, but that could be easily fixed by changin
```
from sh import pdbedit
```
to 
```
import sh
pdbedit = sh.Command("/usr/local/samba/bin/pdbedit")
```
Script also uses python-sh package, so it's on you to satisfy dependencies =)
Well that's probably it.
