KPi on Raspberry Pi Zero W
===================================================================

<br>


Background
-------------------------------------------------------------------

### Basics:

- We use a Kali image written to a microSD card.
- We forego full-disk encryption to ensure remote reboots are seamless.
- Requires minimum class-10 micro SD card of at least 16 GB. Recommend 32 GB for additional tools.

### Future goals of Kali Pi image:

- [ ] Script to pair KPi internal bluetooth with external BT device.
- [ ] Script to associate KPi internal WiFi with external WAP.
- [ ] Script to customize MOTD.
- [ ] Script to make KPi unique via passwds and SSH keys.
- [ ] Launcher scripts for tools.
- [ ] On boot, KPi connects to first pre-paired BT device it sees.
- [ ] On boot, KPi connects to first pre-associated WAP it sees.
- [ ] Pins for JTAG/UART jumper cables.


<br>

Setup
-------------------------------------------------------------------

#### [1] Download.

Download the Kali armel image for Raspberry Pi from <https://www.offensive-security.com/kali-linux-arm-images/>.

#### [2] Extract.

```
# xz -vd kali-2017.01-rpi.img.xz
```

#### [3] Write to SD card.

```
# dc3dd if=kali-2017.01-rpi.img of=/dev/sdX
```

#### [4] Extend `/dev/sdX2` partition and filesystem.

```
# gparted
```

(Following directions refer to the GUI)

- Select the SD card (`/dev/sdX`) in upper righthand corner.
- Right-click the second, larger partition and select `Resize/Move`.
- Drag the endpoint all the way to the end (to the right). Click ‘Resize/Move’.
- `Edit` > `Apply all operations` > `Apply`
- Close gparted.

#### [5] Insert SD card and turn on RPi.

- Put the microSD card into your RPi Zero W.
- Connect micro USB ‘USB’ to an ethernet adapter and connect that to the network.
- Connect KPI micro USB ‘PWR’ to  power source.

#### [6] Connect.

Find your RPi on the network.

```
# nmap --open -Pn -p22 <network/cidr>
```

SSH into your KPi.

```
# ssh root@<ipaddress>
```

#### [7] Configure users.

```
# useradd -m user1
# passwd user1
# usermod -a -G sudo user1
# chsh -s /bin/bash user1
# passwd root
```

#### [8] Reboot and login as user1.

#### [9] Configure more.

Set up hosts file.

```
$ sudo nano /etc/hosts
```

```
127.0.0.1    kpiFML  localhost     # Change the hostname. Don't include this comment
...
# These are remote hosts we manually add:
xxx.yyy.zzz.qqq vpsFML1    # IP address and hostname of VPS, for easier typing
```

Change hostname file.

```
$ sudo nano /etc/hostname
```

```
kpiFML
```

Create new SSH keys (client and server).

```
$ ssh-keygen        <- follow the prompts or just hit enter thru them; user1’s keys
$ sudo rm -v /etc/ssh/ssh_host_*         <- this regenerates the server keys
$ sudo dpkg-reconfigure openssh-server
$ systemctl restart ssh
$ su root
# rm /root/.ssh/*
```

#### [10] Add packages.

```
sudo apt update
sudo apt install -y aircrack-ng armitage broadcom-sta-* cewl cherrytree curl dirbuster exfat-fuse exfat-utils exploitdb gcc gcc-multilib gedit git giskismet googleearth-package gparted gpsd hashcat hashcat-data hashcat-utils hashid john kismet kismet-plugins keepnote libreoffice macchanger maltegoce metasploit-framework mingw-w64* net-tools openvpn pidgin pidgin-otr postgresql powersploit proxychains python-pip rdesktop screen set tcpdump tightvncserver tmux tor torchat unrar vim webshells windows-binaries windows-privesc-check wine winetricks wireshark wordlists x11vnc xfce4-screenshooter xvnc4viewer xzip yersinia zenmap
pip install virtualenv pyftpdlib
```

#### [11] Download and install the Linux version of VeraCrypt.

Go to <https://www.veracrypt.fr/en/Downloads.html> and manually download.

```
$ cd /path/to/veracrypt-XXXX-setup.tar.bz2
$ tar xvf veracrypt-XXXX-setup.tar.bz2
$ cd <created directory>
$ ./<the x86 or 32-bit GUI installation filename>
```

#### [12] Modify the PATH variable.

```
$ sudo echo “PATH DEFAULT=${HOME}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin/X11:/usr/bin/X11” >> /etc/security/pam_env.conf
```

#### [13] Reboot and confirm.

<br>


