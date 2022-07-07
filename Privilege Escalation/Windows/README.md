# Helpful Windows privilege escalation tips

## User enumeration
Current user’s privileges: ```whoami /priv```

List users: ```net users```

List details of a user: ```net user username``` (e.g. net user Administrator)

Other users logged in simultaneously: ```qwinsta``` (the query session command can be used the same way) 

User groups defined on the system: ```net localgroup```

List members of a specific group: ```net localgroup groupname``` (e.g. net localgroup Administrators)

System info : ```systeminfo | findstr /B /C:"OS Name" /C:"OS Version"```

find configuration files: ```findstr /si password *.txt```, or ```.xls, .xml, .ini , etc```

List updates installed on the target system: ```wmic qfe get Caption,Description,HotFixID,InstalledOn```

## Network Connections
```netstat -ano```

## Scheduled tasks
```schtasks /query /fo LIST /v```

## Drivers
```driverquery```

## Antivirus
windows defender: ```sc query windefend```
or another services ```sc queryex type=service```

## DLL Hijacking

In summary, for standard desktop applications, Windows will follow one of the orders listed below depending on if the ```SafeDllSearchMode``` is enabled or not.


If ```SafeDllSearchMode``` is enabled, the search order is as follows:

    The directory from which the application loaded.

    The system directory. Use the ```GetSystemDirectory``` function to get the path of this directory.

    The 16-bit system directory. There is no function that obtains the path of this directory, but it is searched.

    The Windows directory. Use the ```GetWindowsDirectory`` function to get the path of this directory.

    The current directory.

    The directories that are listed in the PATH environment variable. Note that this does not include the per-application path specified by the App Paths registry key. The App Paths key is not used when computing the DLL search path.

If ```SafeDllSearchMode``` is disabled, the search order is as follows:

    The directory from which the application loaded.

    The current directory.

    The system directory. Use the ```GetSystemDirectory``` function to get the path of this directory.

    The 16-bit system directory. There is no function that obtains the path of this directory, but it is searched.

    The Windows directory. Use the ```GetWindowsDirectory``` function to get the path of this directory.

    The directories that are listed in the PATH environment variable. Note that this does not include the per-application path specified by the App Paths registry key. The App Paths key is not used when computing the DLL search path. 

Compiling dll using Mingw: ```x86_64-w64-mingw32-gcc windows_dll.c -shared -o output.dll```
We will have to stop and start the dllsvc service again using the command below: ```sc stop dllsvc & sc start dllsvc```
