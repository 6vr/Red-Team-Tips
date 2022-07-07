Kali Tools
================================================================================

<details>
  <summary><b><u>
  Kali Tools Index
  </u></b></summary>

### Reverse Engineering

apktool, dex2jar, diStorm3, edb-debugger, jad, javasnoop, JD-GUI, OllyDbg, smali, Valgrind, YARA

### Reporting Tools

CaseFile, CutyCapt, dos2unix, Dradis, KeepNote, MagicTree, Metagoofil, Nipper-ng, pipal

### Stress Testing

DHCPig, FunkLoad, iaxflood, Inundator, inviteflood, ipv6-toolkit, mdk3, Reaver, rtpflood, SlowHTTPTest, t50, Termineter, THC-IPV6, THC-SSL-DOS

### Forensics Tools

Binwalk, bulk-extractor, Capstone, chntpw, Cuckoo, dc3dd, ddrescue, DFF, diStorm3, Dumpzilla, extundelete, Foremost, Galleta, Guymager, iPhone Backup Analyzer, p0f, pdf-parser, pdfid, pdgmail, peepdf, RegRipper, Volatility, Xplico

### Hardware Hacking

android-sdk, apktool, Arduino, dex2jar, Sakis3G, smali

### Maintaining Access

CryptCat, Cymothoa, dbd, dns2tcp, http-tunnel, HTTPTunnel, Intersect, Nishang, polenum, PowerSploit, pwnat, RidEnum, sbd, U3-Pwn, Webshells, Weevely, Winexe

### Wireless Attacks

Aircrack-ng, Asleap, Bluelog, BlueMaho, Bluepot, BlueRanger, Bluesnarfer, Bully, coWPAtty, crackle, eapmd5pass, Fern Wifi Cracker, Ghost Phisher, GISKismet, Gqrx, gr-scan, hostapd-wpe, kalibrate-rtl, KillerBee, Kismet, mdk3, mfcuk, mfoc, mfterm, Multimon-NG, PixieWPS, Reaver, redfang, RTLSDR Scanner, Spooftooph, Wifi Honey, wifiphisher, Wifitap, Wifite

### Web Applications

apache-users, Arachni, BBQSQL, BlindElephant, Burp Suite, CutyCapt, DAVTest, deblaze, DIRB, DirBuster, fimap, FunkLoad, Gobuster, Grabber, jboss-autopwn, joomscan, jSQL, Maltego Teeth, PadBuster, Paros, Parsero, plecost, Powerfuzzer, ProxyStrike, Recon-ng, Skipfish, sqlmap, Sqlninja, sqlsus, ua-tester, Uniscan, Vega, w3af, WebScarab, Webshag, WebSlayer, WebSploit, Wfuzz, WPScan, XSSer, zaproxy

### Exploitation Tools

Armitage, Backdoor Factory, BeEF, cisco-auditing-tool, cisco-global-exploiter, cisco-ocs, cisco-torch, Commix, crackle, exploitdb, jboss-autopwn, Linux Exploit Suggester, Maltego Teeth, Metasploit Framework, RouterSploit, SET, ShellNoob, sqlmap, THC-IPV6, Yersinia

### Password Attacks

Burp Suite, CeWL, chntpw, cisco-auditing-tool, CmosPwd, creddump, crunch, DBPwAudit, findmyhash, gpp-decrypt, hash-identifier, HexorBase, THC-Hydra, John the Ripper, Johnny, keimpx, Maltego Teeth, Maskprocessor, multiforcer, Ncrack, oclgausscrack, PACK, patator, phrasendrescher, polenum, RainbowCrack, rcracki-mt, RSMangler, SQLdict, Statsprocessor, THC-pptp-bruter, TrueCrack, WebScarab, wordlists, zaproxy

### ReconInTrace, iSMTP, lbd, Maltego Teeth, masscan, Metagoofil, Miranda, nbtscan-unixwiz, Nmap, ntop, p0f, Parsero, Recon-ng, SET, smtp-user-enum, snmp-check, SPARTA, sslcaudit, SSLsplit, sslstrip, SSLyze, THC-IPV6, theHarvester, TLSSLed, twofi, URLCrazy, Wireshark, WOL-E, Xplico

### Vulnerability Analysis

BBQSQL, BED, cisco-auditing-tool, cisco-global-exploiter, cisco-ocs, cisco-torch, copy-router-config, DBPwAudit, Doona, DotDotPwn, HexorBase, Inguma, jSQL, Lynis, Nmap, ohrwurm, Oscanner, Powerfuzzer, sfuzz, SidGuesser, SIPArmyKnife, sqlmap, Sqlninja, sqlsus, THC-IPV6, tnscmd10g, unix-privesc-check, Yersinia

### Sniffing & Spoofing

Burp Suite, DNSChef, fiked, hamster-sidejack, HexInject, iaxflood, inviteflood, iSMTP, isr-evilgrade, mitmproxy, ohrwurm, protos-sip, rebind, responder, rtpbreak, rtpinsertsound, rtpmixsound, sctpscan, SIPArmyKnife, SIPp, SIPVicious, SniffJoke, SSLsplit, sslstrip, THC-IPV6, VoIPHopper, WebScarab, Wifi Honey, Wireshark, xspy, Yersinia, zaproxy

<br>
</details>

<details>
  <summary><b><u>
  Non-Kali Tools
  </u></b></summary>

* Mana
* Powershell Empire (Linux)
* Snoopy-ng (Linux)
* Scrapy (Py)
* Mimikatz (Py)
* wmi_info.bat (SA)
* PsTools.exe (SA)
* Fgdump.exe (SA)
* tftp.exe (SA)
* wget (BI & SA)
* WinSCP (SA)
* Putty (SA)
* HyperTerm (SA)
* TerraTerm (SA)
* Reg.exe (BI)
* Cygwin+tools

<br>
</details>


Details
================================================================================

## upx

Ultimate Packer for Executables (UPX) compresses PEs for transfer to victim.

```
root@kali:~# upx -9 nc.exe
```

## Automater

Query sites for info on IP, URL, or hash. 

```
root@kali:~# automater <IP|URL|hash>
```

## bing-ip2hosts

Use Bing to find websites at an IP and hostnames in a domain. Find attack surfaces.

```
root@kali:~# bing-ip2hosts -p <IP|domain_name>
```

## DNSRecon

Brute force domain hosts. DNS info on IP ranges and domains. 

```
root@kali:~# dnsrecon –r <CIDR_network>
root@kali:~# dnsrecon –d example.com –D wordlist.txt –t std
```

## DotDotPwn

Fuzzer to find and employ directory traversal vuls in ftp, http, tftp.

```
root@kali:~# dotdotpwn –m ftp –h <host> -x <port> -o <OS> -E –U <user> -P <pw>
```

## enum4linux

Gathers system information from SMB null sessions.

```
root@kali:~# enum4linux [-u <user>] [-p <pw> <tgt.ip> > <output_file>
```

## Ghost Phisher

Emulate WAPs, do MITM, locally phish, hijack sessions, log creds. (GUI)

```
root@kali:~# ghost-phisher
```

## goofile

Search for specific file type in a domain.

```
root@kali:~# goofile –d example.com –f <filetype_extension>
```

## hping3

Craft TCP, UDP, ICMP, and RAW-IP packets. Spoof source IP. Xfr data through covert channel.

```
root@kali:~# hping3 host [options]
  -h  --help      show this help
  -v  --version   show version
  -c  --count     packet count
  -i  --interval  wait (uX for X microseconds, for example -i u1000)
      --fast      alias for -i u10000 (10 packets for second)
      --faster    alias for -i u1000 (100 packets for second)
      --flood	   sent packets as fast as possible. Don't show replies.
  -n  --numeric   numeric output
  -q  --quiet     quiet
  -I  --interface interface name (otherwise default routing interface)
  -V  --verbose   verbose mode
  -D  --debug     debugging info
  -z  --bind      bind ctrl+z to ttl           (default to dst port)
  -Z  --unbind    unbind ctrl+z
      --beep      beep for every matching packet received
Mode
  default mode     TCP
  -0  --rawip      RAW IP mode
  -1  --icmp       ICMP mode
  -2  --udp        UDP mode
  -8  --scan       SCAN mode.
                   Example: hping --scan 1-30,70-90 -S www.target.host
  -9  --listen     listen mode
IP
  -a  --spoof      spoof source address
  --rand-dest      random destionation address mode. see the man.
  --rand-source    random source address mode. see the man.
  -t  --ttl        ttl (default 64)
  -N  --id         id (default random)
  -W  --winid      use win* id byte ordering
  -r  --rel        relativize id field          (to estimate host traffic)
  -f  --frag       split packets in more frag.  (may pass weak acl)
  -x  --morefrag   set more fragments flag
  -y  --dontfrag   set don't fragment flag
  -g  --fragoff    set the fragment offset
  -m  --mtu        set virtual mtu, implies --frag if packet size > mtu
  -o  --tos        type of service (default 0x00), try --tos help
  -G  --rroute     includes RECORD_ROUTE option and display the route buffer
  --lsrr           loose source routing and record route
  --ssrr           strict source routing and record route
  -H  --ipproto    set the IP protocol field, only in RAW IP mode
ICMP
  -C  --icmptype   icmp type (default echo request)
  -K  --icmpcode   icmp code (default 0)
      --force-icmp send all icmp types (default send only supported types)
      --icmp-gw    set gateway address for ICMP redirect (default 0.0.0.0)
      --icmp-ts    Alias for --icmp --icmptype 13 (ICMP timestamp)
      --icmp-addr  Alias for --icmp --icmptype 17 (ICMP address subnet mask)
      --icmp-help  display help for others icmp options
UDP/TCP
  -s  --baseport   base source port             (default random)
  -p  --destport   [+][+]<port> destination port(default 0) ctrl+z inc/dec
  -k  --keep       keep still source port
  -w  --win        winsize (default 64)
  -O  --tcpoff     set fake tcp data offset     (instead of tcphdrlen / 4)
  -Q  --seqnum     shows only tcp sequence number
  -b  --badcksum   (try to) send packets with a bad IP checksum
                   many systems will fix the IP checksum sending the packet
                   so you'll get bad UDP/TCP checksum instead.
  -M  --setseq     set TCP sequence number
  -L  --setack     set TCP ack
  -F  --fin        set FIN flag
  -S  --syn        set SYN flag
  -R  --rst        set RST flag
  -P  --push       set PUSH flag
  -A  --ack        set ACK flag
  -U  --urg        set URG flag
  -X  --xmas       set X unused flag (0x40)
  -Y  --ymas       set Y unused flag (0x80)
  --tcpexitcode    use last tcp->th_flags as exit code
  --tcp-mss        enable the TCP MSS option with the given value
  --tcp-timestamp  enable the TCP timestamp option to guess the HZ/uptime
Common
  -d  --data       data size                    (default is 0)
  -E  --file       data from file
  -e  --sign       add 'signature'
  -j  --dump       dump packets in hex
  -J  --print      dump printable characters
  -B  --safe       enable 'safe' protocol
  -u  --end        tell you when --file reached EOF and prevent rewind
  -T  --traceroute traceroute mode              (implies --bind and --ttl 1)
  --tr-stop        Exit when receive the first not ICMP in traceroute mode
  --tr-keep-ttl    Keep the source TTL fixed, useful to monitor just one hop
  --tr-no-rtt	    Don't calculate/show RTT information in traceroute mode
ARS packet description (new, unstable)
  --apd-send       Send the packet described with APD (see docs/APD.txt)
```

## ident-user-enum

Find out which user a TCP service is running as (e.g., as root).

```
root@kali:~# ident-user-enum <remote_ip> <port1> <port2> <port3> ....
```

## CDPSnarf

Sniffs traffic and extracts informative Cisco Discovery Protocol (CDP) traffic and info.

```
root@kali:~# cdpsnarf –i eth0 –w output.pcap          <-- Live capture
root@kali:~# cdpsnarf –r input.pcap –w output.pcap    <-- Past capture
```

## cisco-torch

Scan & attack Cisco devices. 

```
root@kali:~# cisco-torch –A <cidr_network>             <-- Scan
root@kali:~# cisco-torch –s –u –c –w –j –t –b –g <IP>  <-- Dict attack & get configs
```

## acccheck

Dictionary attack for Windows auth via SMB.

```
root@kali:~# acccheck -v –t <tgt.ip> -u <user> -P <wordlist>
```

## amap

Application Mapper – Positively ID services, regardless of port, by sending packets and analyzing replies. 

```
root@kali:~# amap –bqv <tgt.ip> <port1> <port2> ...  <-- TCP
root@kali:~# amap –bqvu <tgt.ip> <port1> <port2> ... <-- UDP
```



<br>