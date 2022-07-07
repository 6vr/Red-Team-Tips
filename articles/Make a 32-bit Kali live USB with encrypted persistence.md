Make a 32-bit Kali Live USB with Encrypted Persistence
================================================================================

Notes
--------------------------------------------------------------------------------
* Kali on a live USB increases portability and aids physical-access attacks on a target host.
* Use a 32-bit version to ensure it works even on old computers.
* Encrypted persistence maintains confidentiality and retains installed tools and updates.
* USB 3.x significantly improves usability, but ensure drives are backwards compatible with older USB standards.
* Have successfully tested this on a microSD card running in a USB 3.0 adapter, but filesystems occasionally turn read-only for the duration of the session. I avoid microSD now.
* Minimum recommended drive capacity is 32GB.

*The URLs below will change with new roll-outs of Kali.*

Steps
--------------------------------------------------------------------------------
### [1] - Download Kali Lite 32-bit image and verify that its SHA256 sum matches the GPG-signed sum provided by Offensive Security. 

You'll use the main GPG web server as the trusted source for Offensive Security's public keys.

I only provide these instructions for Linux systems. An alternative for any OS is to find the file on kali.org, download it, and do your best to confirm its authenticity with GPGTools or GPG4Win.

```
user@linux:~$ mkdir TempWorkingDir && cd TempWorkingDir
user@linux:~$ wget http://cdimage.kali.org/kali-2017.1/kali-linux-light-2017.1-i386.iso
user@linux:~$ sha256sum kali-linux-light-2017.1-i386.iso | cut -d" " -f 1 > myfile.sum

user@linux:~$ gpg --keyserver hkp://keys.gnupg.net --recv-key 7D8D0BF6
user@linux:~$ gpg --fingerprint 7D8D0BF6
user@linux:~$ wget http://cdimage.kali.org/kali-2017.1/SHA256SUMS.gpg

user@linux:~$ gpg --verify SHA256SUMS.gpg SHA256SUMS
```

### [2] Identify the correct USB drive and write/burn the Kali ISO to it.
 
#### -----[2.A] Working in Linux.

```
user@linux:~$ sudo fdisk -l
user@linux:~$ sudo dc3dd if=/path/to/kali.iso of=/dev/sdX 
   OR
user@linux:~$ sudo dd if=/path/to/kali.iso of=/dev/sdX bs=1M
```

#### ----[2.B] Working in Mac OS.

```
user@mac:~$ diskutil list
user@mac:~$ sudo dc3dd if=/path/to/kali.iso of=/dev/diskX
   OR
user@mac:~$ sudo dd if=/path/to/kali.iso of=/dev/diskX bs=1M
```

#### ----[2.C] Working in Windows.
* Download win32diskimager.exe and follow the GUI instructions.

### [3] Repartition the disk.

*Note: For this and future steps, I recommend working from within a Kali or other Linux environment. You could achieve the same endstate from within MacOS or Windows, but tool and command consistency across Debian/Ubuntu Linux variants greatly simplifies the process. All commands assume a Linux distro working environment.*

```
user@linux:~$ sudo parted
 GNU Parted 2.3
 Using /dev/sda
 Welcome to GNU Parted! Type 'help' to view a list of commands.

(parted) print devices                                                    
 /dev/sda (480GB)
 /dev/sdb (31.6GB)

(parted) select /dev/sdb     // <---- Or whichever /dev/sdX is your USB!
 Using /dev/sdb

(parted) print                                                            
 Model: SanDisk SanDisk Ultra (scsi)
 Disk /dev/sdb: 31.6GB
 Sector size (logical/physical): 512B/512B
 Partition Table: msdos
 
 Number  Start   End     Size    Type     File system  Flags
  1      32.8kB  2988MB  2988MB  primary               boot, hidden
  2      2988MB  3050MB  64.9MB  primary  fat16

(parted) mkpart primary 3050                                        
(parted) quit                                                             
 Information: You may need to update /etc/fstab.
```

### [4] Set up encryption and persistence.

*Note: Obviously, retain the passphrase you choose for this encryption setup. You need it to boot in the future.*

```
user@linux:~$ cryptsetup --verbose --verify-passphrase luksFormat /dev/sdb3
user@linux:~$ cryptsetup luksOpen /dev/sdb3 my_usb
user@linux:~$ mkfs.ext3 /dev/mapper/my_usb
user@linux:~$ e2label /dev/mapper/my_usb persistence
user@linux:~$ mkdir -p /mnt/my_usb
user@linux:~$ mount /dev/mapper/my_usb /mnt/my_usb
user@linux:~$ echo "/ union" > /mnt/my_usb/persistence.conf
user@linux:~$ umount /dev/mapper/my_usb
user@linux:~$ cryptsetup luksClose /dev/mapper/my_usb
```

*Now your USB stick is ready to plug in and reboot into Live USB Encrypted Persistence mode.*

### [5] The two useful Kali live boot options you'll use.

Restart the computer and cause it to boot from the USB. Sometimes you have to enable USB-boot in the BIOS. Sometimes it will automatically boot to USB ahead of internal HDD. Most often, you need to manually select to boot from USB in the boot menu. <kbd>F12</kbd>, <kbd>F11</kbd>, and <kbd>option</kbd> are usual boot-choice keys.

#### -----[5.A] Useful boot option #1: Live

Once the Kali boot menu (splash page) appears, select "Kali Live", which is usually the top-most option. This mode retains no changes to your Kali operating system, but you can temporarily store data in memory. For example, you can install packages to use for that session, but they will disappear on reboot. 

This mode is most useful when booting an untrusted computer from your Kali USB in order to prevent malicious modification of your USB. Unfortunately, you will have few tools available since we started with a Kali Lite ISO. If you use this mode frequently, perhaps you want the additional tools available in a full Kali distribution.

In this mode, the default root password is ‘toor’ without quotes.

#### -----[5.B] Useful boot option #2: Encypted persistence

At the splash page, scroll down to the option with encrypted persistence. (Note--this is not the same as persistence without encryption, which I do not recommend you use.)

Once you select encrypted persistence, the system will initiate its boot process. It will pause at a cryptsetup prompt, asking you to enter the correct passphrase. This is the passphrase you chose when you created your encrypted partition. Entering the passphrase and hitting enter will unlock your encryption key in memory, which allows the kernel to read and mount the enclosed filesystem. The data itself remains encrypted on the USB drive and is only decrypted on-the-fly when loaded in memory.

You can use apt to install and upgrade packages. You can save data. You can set system services. Basically, this is a completely-usable operating system, with all changes retained (and encrypted) between boots. The only caveat is that you can run out of storage capacity quickly.

### [6] Configure your encrypted, persistent Kali OS.

Boot into your Kali USB's encrypted persistent OS. You'll use the default root password of 'toor' without quotes.

Change the root password. Then create a new sudoer user. You should always use this user from now on. In the commands below, I create a user named 'user0'.

*For those of you who tire of typing `sudo` before every major command, remember that `sudo -i` and `su` are commands to give you root terminals.*

```
root@kali:~# passwd
root@kali:~# useradd -m user0
root@kali:~# passwd user0
root@kali:~# usermod -a -G sudo user0
root@kali:~# chsh -s /bin/bash user0
```

Now log out or reboot. Log back in using user0.

Add some packages from repo. You can copy+paste the below, which is a single command-line entry.

```
user0@kali:~$ sudo apt update
user0@kali:~$ sudo apt install -y aircrack-ng armitage broadcom-sta-* cewl cherrytree curl dc3dd dirbuster exfat-fuse exfat-utils exploitdb gcc gcc-multilib gedit git giskismet googleearth-package gparted gpsd hashcat hashcat-data hashcat-utils hashid john kismet kismet-plugins keepnote libreoffice macchanger maltegoce metasploit-framework mingw-w64* net-tools openvpn pidgin pidgin-otr postgresql powersploit python-pip rdesktop screen set tcpdump tightvncserver tmux tor torchat unrar vim webshells windows-binaries windows-privesc-check wine winetricks wireshark wordlists x11vnc xfce4-screenshooter xvnc4viewer xzip yersinia zenmap
```

Add some packages with Pip.

```
user@kali:~$ pip install virtualenv pyftpdlib
```

Download and install the Linux version of VeraCrypt. Go to <https://www.veracrypt.fr/en/Downloads.html> and manually download it.

```
user0@kali:~$ tar xvf /path/to/veracrypt-XXXX-setup.tar.bz2
user0@kali:~$ cd /path/to/new-directory
user0@kali:/path/to/new-directory$ ./<x86 GUI install file>
```

Launch Firefox and install the following extensions/add-ons:

* Tamper Data
* Cookies Manager+

Modify the `PATH` variable. Copy and paste the following, single command.

```
user0@kali:~$ sudo echo “PATH DEFAULT=${HOME}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin/X11:/usr/bin/X11” >> /etc/security/pam_env.conf
```

***TO BE COMPLETED: Add some other packages manually. proxychains-ng, python pwn tools, snoopy-ng, or my football with install script.***
