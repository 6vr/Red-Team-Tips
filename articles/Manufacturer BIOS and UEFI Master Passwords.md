Manufacturer BIOS and UEFI Master Passwords
================================================================================

<br>

### About

Newer BIOS and UEFI systems are not vulnerable to 'pull battery and wait' or 'short the pins' attacks. Credentials are stored in NVRAM and no longer blank or drop via manual exploit.

One way to defeat BIOS/UEFI password protection is to try manufacturer passwords. Computer manufacturers often hard-code bypass and master passwords into their own branded BIOS/UEFI platforms. They use the passwords for ease of utility during setup, but employees and crackers often discover and leak the passwords. In an attempt to discourage such cracks, manufacturers began to implement password-generation schemes by which individual computers would have different, yet reproducible BIOS/UEFI passwords. Fortunately for us, the data used to reproduce the passwords are openly stored on the computers themselves, often incorporating combinations of serial number, model number, and so on. Now, crackers simply need a copy of the password generation algorithm and can create the appropriate master password for any specific system.

<br>

### Web Resource

A good source for BIOS and UEFI master passwords is <https://bios-pw.org/>. I last used this site in November 2017 with great success. Take note of additional instructions beneath the generated master passwords, particularly instructions such as, "For some Dell systems you must hit <kbd>ctrl</kbd>+<kbd>enter</kbd> as opposed to just <kbd>enter</kbd> for the password to work."

<br>

<details>
  <summary><b><u>
  Incomplete List of Manufacturer Passwords
  </u></b></summary>

### Incomplete List of Manufacturer Passwords

(Case sensitive.)

#### Phoenix Backdoor BIOS Passwords:

* BIOS
* CMOS
* phoenix
* PHOENIX

#### AMI BIOS Backdoor Passwords:

* A.M.I.
* AAAMMMII
* AMI
* AMI?SW
* AMI_SW
* BIOS
* CONDO
* HEWITT RAND
* LKWPETER
* MI
* Oder
* PASSWORD

#### Award BIOS Backdoor Passwords:

* (eight spaces)
* 01322222
* ALFAROME
* 589589
* 589721
* 595595
* 598598 
* ALLY
* ALLy
* aLLY
* aLLy
* aPAf
* award
* awkward
* IOSTAR
* CONCAT
* CONDO
* Condo
* condo
* d8on
* djonet
* HLT
* J256
* J262
* j262
* j322
* j332
* J64
* KDD
* LKWPETER
* Lkwpeter
* PINT
* pint
* SER
* SKY_FOXSYXZ
* SKY_FOX
* syxz
* SYXZ
* TTPTHA
* ZAAAADA
* ZAAADA
* ZBAAACA
* ZJAAADC
* AWARD PW
* AWARD SW
* AWARD?SW
* AWARD_PW
* AWARD_SW
* AWKWARD

#### Other: (Manufacturer name – password)

* VOBIS and IBM – merlin
* Dell – Dell
* Biostar – Biostar
* Compaq – Compaq
* Enox – xo11nE
* Epox – central
* Freetech – Posterie
* IWill – iwill
* Jetway – spooml
* Packard Bell – bell9
* QDI – QDI
* Siemens – SKY_FOX
* SOYO – SY_MB
* TMC – BIGO
* Toshiba – Toshiba

<br>
</details>