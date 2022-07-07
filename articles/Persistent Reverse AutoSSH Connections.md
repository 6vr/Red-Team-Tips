Persistent Reverse AutoSSH Connections
================================================================================

<br>

***NOTE: Example ports are indicated by placing a port number inside angle brackets `<` and `>`. Do not include the angle brackets in your commands, and do not feel restricted to the example port numbers.***

<br>

<details>
  <summary><b><u>
  Windows Client with Cygwin
  </u></b></summary>

Download one: 
* <https://cygwin.com/setup-x86.exe>
* <https://cygwin.com/setup-x86_64.exe>

Run it. Select ‘Install from Internet’. Choose Auto SSH, Open SSH, Open SSL, Zip, Unzip.

Allow Cygwin Setup to resolve dependencies.

Launch Cygwin[64] Terminal from Start Menu.

Create your RSA key pair and upload to jumpbox.

```
cygwin$ ssh-host-config
cygwin$ cygrunsrv –S sshd
cygwin$ cygrunsrv --query sshd
cygwin$ ssh-keygen
cygwin$ scp .ssh/id_rsa.pub share@<jumpboxIP>:~/addme.pub
cygwin$ ssh user@<jumpboxIP>    
      // You'll have to accept the server with 'yes' and then enter the pw
      
user@jumpbox:~$ cat addme.pub >> ~/.ssh/authorized_keys
user@jumpbox:~$ rm addme.pub
user@jumpbox:~$ exit
```

Test passwordless logon.

```
cygwin$ ssh user@<jumpboxIP>
     // You should NOT have to enter your pw

user@jumpbox:~$ exit
```

Set up the AutoSSH service to run in Cygwin.

```
cygwin$ cygrunsrv -I AutoSSH -p /path/to/autossh -a "-M <60000> -N -n -R <60001>:localhost:22 user@<jumpboxID> -e AUTOSSH_NTSERVICE=yes
cygwin$ exit
```

</details>

<details>
  <summary><b><u>
  Debian Linux Client Using systemd
  </u></b></summary>
  
SSH RSA key prep

```
<client_user>@linux:~$ ssh-keygen
<client_user>@linux:~$ ssh-copy-id user@<jumpboxIP>
```

OpenSSH Server reconfiguration (Optional--intended for pre-installed OpenSSH Server)

```
<client_user>@linux:~$ sudo rm –v /etc/ssh/ssh_host_*
<client_user>@linux:~$ sudo dpkg-reconfigure openssh-server
<client_user>@linux:~$ sudo systemctl restart ssh
```

```
<client_user>@linux:~$ sudo apt update
<client_user>@linux:~$ sudo apt install –y openssh-server autossh tmux vim
```

```
<client_user>@linux:~$ sudo vim /etc/systemd/system/autossh-reverse.service
```

Add contents to unit file, with no broken lines

```
[Unit]
Description=Reverse SSH tunnel to this system.
After=multi-user.target

[Service]
ExecStart=/usr/bin/autossh -M <60000> -N -n -R <60001>:localhost:22 user@<jumpboxIP>
User=<client_user>

[Install]
WantedBy=multi-user.target
```

```
<client_user>@linux:~$ sudo systemctl daemon-reload
<client_user>@linux:~$ sudo systemctl start autossh-reverse.service
<client_user>@linux:~$ sudo systemctl enable autossh-reverse.service
```

</details>

<details>
  <summary><b><u>
  Debian Linux Client Using rc.local
  </u></b></summary>

SSH RSA key prep

```
<client_user>@linux:~$ ssh-keygen
<client_user>@linux:~$ ssh-copy-id user@<jumpboxIP>
```

OpenSSH Server reconfiguration (Optional--intended for pre-installed OpenSSH Server)

```
<client_user>@linux:~$ sudo rm –v /etc/ssh/ssh_host_*
<client_user>@linux:~$ sudo dpkg-reconfigure openssh-server
<client_user>@linux:~$ sudo systemctl restart ssh
```

```
<client_user>@linux:~$ sudo apt update
<client_user>@linux:~$ sudo apt install –y openssh-server autossh tmux vim
```

Edit the rc.local file.
  
```
<client_user>@linux:~$ sudo vim /etc/rc.local
```

Add to rc.local as one single line

```
/usr/bin/autossh –M <60000> –f –N –n –R <60001>:localhost:22 user@<jumpboxIP> &
```

```
<client_user>@linux:~$ sudo chmod +x /etc/rc.local
```

</details>

<details>
  <summary><b><u>
  From the Jump Box
  </u></b></summary>

To Execute

```
user@jumpbox:~$ ssh <client_user|root>@localhost –p <60001>
```

</details>

<br>

