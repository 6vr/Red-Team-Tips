Metasploit
===================================================================

<br>

Standard start-up
-------------------------------------------------------------------

```
root@kali:~# service postgresql start
root@kali:~# msfdb init     # <-- Only req’d at first run
root@kali:~# msfconsole
```

You are now in MSF

```
msf > db_status                       (Ensure “postgresql connected to msf”)
msf > workspace -a NewWorkspaceName
msf > workspace                       (Ensure you're in the right one)

msf > db_import /path/to/xml/scans    (If you have any already)
msf > hosts                           (Confirm existing database loaded)
```

<br>

How-to: OpenVAS with MSF on CLI
-------------------------------------------------------------------

*Get help via `openvas_help` if needed.*

*OpenVAS is a vulnerability scanner and is* ***LOUD***.

#### [1] Load OpenVAS inside MSF.

```
msf > load openvas
msf > openvas-setup
  ...
  User created with password 'bdd8a10c-90c4-40fd-8319-dd3f42240871'.

msf > openvas_connect admin bdd8a10c-90c4-40fd-8319-dd3f42240871   
  ...
  [+] OpenVAS connection successful
```

#### [2] Set up your OpenVAS target and preferences.

```
msf > openvas_target_create "10.11.1.125" 10.11.1.125 "Checking Acritum ftp server"
  ...
  ID                                    Name         Hosts        
  b493b7a8-7489-11df-a3ec-002264764cea  Localhost    localhost    ...
  df0a4bcf-1508-45ad-8c5e-c01b6c068c8b  10.11.1.125  10.11.1.125  ...

msf > openvas_config_list
  ...
  ID                                    Name
  2d3f051c-55ba-11e3-bf43-406186ea4fc5  Host Discovery
  698f691e-7489-11df-9d8c-002264764cea  Full and fast ultimate  
  708f25c4-7489-11df-8094-002264764cea  Full and very deep

msf > openvas_task_create "10.11.1.125" "ftp server" 698f691e-... df0a4bcf-
  ...
  ID                                    Name         Comment          ...
  31a18432-73d6-41a2-8d0a-ec203b1b9915  10.11.1.125  Checking Acritum ...
```

### [3] Start the scan.

```
msf > openvas_task_start 31a18432-73d6-41a2-8d0a-ec203b1b9915
  ...
```

#### [4] Check for completion (progress == -1).

```
msf > openvas_task_list 
  ...
  31a18432-73d6-41a2-8d0a-ec203b1b9915  10.11.1.125  Checking Acritum ...
```

#### [5] Import results to MSF.

```
msf > openvas_report_list 
  ...
  ID                                    Task Name    Start Time    ...
  7b2d443d-1dff-4c27-add2-52c756cd6968  10.11.1.125  2016-12-12T16:
 
msf > openvas_format_list 
  ...
  ID                                    Name           Extension  Summary
  a994b278-1f62-11e1-96ac-406186ea4fc5  XML            xml        Raw ...

msf > openvas_report_import <reportID> <reportformat>
  ...
```

#### [6] Optional. Download OpenVAS scan report.

```
msf > openvas_report_list 
msf > openvas_format_list 
msf > openvas_report_download <reportID> <reportformat> <dest/dir>
```

<br>

How-to: OpenVAS with MSF using Greenborne Security Assistant
-------------------------------------------------------------------

#### [1] Load OpenVAS inside MSF.

```
msf > load openvas
msf > openvas-setup
  ...
  User created with password 'bdd8a10c-90c4-40fd-8319-dd3f42240871'.
```

#### [2] Browser.

Go to <https://127.0.0.1:9392>. 

Log in with ‘admin’ = 'bdd8a10c-90c4-40fd-8319-dd3f42240871' <-- (pw from above)

#### [3] Scan.

`Configuration` > `Targets`. Create a new target.

`Scan Management` > `Tasks`. Create a new task.

`Scan Management` > `Tasks`. Run the task.

#### [4] Get the report.

`Scan Management` > `Reports`. Select the task/report.

Export the report in plain old XML format.

```
msf > db_import /path/to/your/report/file.xml
```

<br>

Exploit choice construction
-------------------------------------------------------------------

<br>

Payload choice construction
-------------------------------------------------------------------

<br>

Run-through
-------------------------------------------------------------------

Run-through of start-up, ID, portscan, vulscan, exploit, meterpreter

<br>

Meterpreter
-------------------------------------------------------------------

<br>

Pivoting
-------------------------------------------------------------------

<br>

Tools outside the console
-------------------------------------------------------------------

### pattern\_create.rb & pattern\_offset.rb

Used for fuzzing programs to identify the offset to overflow a buffer. Use pattern\_create to generate a long string of characters with a unique pattern. Send that string to your target application using whatever script or user interface you've created while running a debugger attached to the target application. Look at the register of interest and copy the four or however many bytes it holds. Use pattern\_offset to determine how much filler data preceded that register's contents. The result is your offset.

```
root@kali:~# pattern_create.rb
  -l    Length of data buffer to create

root@kali:~# pattern_offset.rb
  -l    Length of data buffer that you used (assumes created by above)
  -q    The pattern you see in the register
```

Example:

```
root@kali:~# /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2700
  Aa0Aa1Aa2Aa3....
```

Send that string to the application as user input. Record the contents of the EIP or other register you want in debugger.

```
root@kali:~# /usr/share/met...rk/tools/exploit/pattern_offset.rb -l 2700 -q 39694438
  [*] Exact match at offset 2606
```

Use fill of `\x41` * 2606 followed by four EIP bytes (little endian) in your exploit.


<br>

Porting modules to python/ruby standalone
-------------------------------------------------------------------

<br>

