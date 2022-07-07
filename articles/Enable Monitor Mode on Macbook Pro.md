Enable Monitor Mode on Macbook Pro
================================================================================

Notes
--------------------------------------------------------------------------------
* This only works for MBPs with BCM4360 wireless cards.
* This does not enable packet injection--only monitor mode.
* Instead of creating interface `wlan0mon`, airmon-ng will create `prism0`. Take note of which commands require `wlan0` or `prism0`.
* Do this after configuring your Kali OS, including updating package lists and installing recommended packages.

Steps
--------------------------------------------------------------------------------

```
user0@kali:~$ sudo modprobe wl
user0@kali:~$ echo “wl” | sudo tee -a /etc/modules
user0@kali:~$ ifconfig
```

You should then see wireless adapter.

Test airmon-ng:

```
user0@kali:~$ sudo airmon-ng start wlan0
user0@kali:~$ sudo airodump-ng prism0
```

As long as it’s in monitor mode, you’re good. Shut down airodump-ng with <kbd>ctrl</kbd>+<kbd>C</kbd>.

```
user0@kali:~$ sudo airmon-ng stop wlan0
```
