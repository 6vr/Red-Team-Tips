Identify & Enumerate SNMP Targets
================================================================================

<br>

### Find systems using SNMP

```
root@kali:~# for ip in $(seq 1 254);do echo 10.11.1.$ip;done > ips.txt
root@kali:~# onesixtyone -c /usr/share/doc/onesixtyone/dict.txt -i ips.txt | tee -a raw.txt
root@kali:~# cat raw.txt | tail -n +2 | cut -d" " -f 1 > snmp_finds.txt
root@kali:~# cat snmp_finds.txt
  10.11.1.13
  10.11.1.14
  10.11.1.22
  ...
```

### Gather information about identified targets

Use **snmp-check** to gather information about the discovered targets. You should know which community terms are valid from the previous step. You might need to guess/fiddle with SNMP version (-v option). Note that these enumerations can take several minutes each.

**This can <u>definitely</u> be scripted, but first need to document the process.**

```
root@kali:~# mkdir snmp-check
root@kali:~# tgts = `cat snmp_finds.txt`
root@kali:~# comm = <public>    // First working community term
root@kali:~# for ip in $tgts; do snmp-check -c $comm -v1 $ip > snmp-check/$ip-$comm.txt; done

  [wait]

root@kali:~# comm = <Next community. Repeat until complete.>
root@kali:~# for ip in $tgts; do snmp-check -c $comm -v1 $ip > snmp-check/$ip-$comm.txt; done

  [wait]

root@kali:~# more snmp-check/*.txt
  snmp-check v1.9 - SNMP enumerator
  Copyright (c) 2005-2015 by Matteo Cantoni (www.nothink.org)
  
  [+] Try to connect to 10.11.1.128:161 using SNMPv1 and community 'public'
  
  [*] System information:
  
  Host IP address               : 10.11.1.128
  Hostname                      : DJ
  Description                   : Hardware: x86...  Windows 2000 ...
  Contact                       : -
  ...
```

<br>

### Alternative Tools

```
# nmap -sU --open -p 161 10.11.1.1-254 -oG snmp-nmap.txt
```

```
# comm = <community>; for ip in $tgts; do snmpwalk -c $comm -v1 $ip > snmpwalk/$ip-$comm.txt; done
```

<br>