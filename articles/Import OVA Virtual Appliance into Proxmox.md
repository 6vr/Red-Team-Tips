Import .ova virtual appliance into Proxmox
===================================================================

Background
-------------------------------------------------------------------

"OVA" stands for "Open Virtual Appliance", and it is an open-source standard for describing and transmitting virtual machines and their runtime states. OVAs typically have the file extension ".ova" and follow the OVA standard, for the most part. OVAs can contain one or numerous VMs in any off or running states.

For your purposes, think of an OVA as a fancy ZIP file or tarball that contains the contents of and metainformation about one or more VMs. At minimum, you want the virtual hard disk file (the VM's HDD) and the OVF or other file that indicates quantity of CPU cores and memory for each VM in the OVA.

Note that virtual hard disks can be in multiple formats depending on the creating software and user preference. Virtualbox by default makes VDIs but can run almost any common format. VMWare client hypervisors typically use VMDKs. Windows often produces VHDs. Lastly, as a type 1 hypervisor, Proxmox leverages full hardware capability and allocates /dev/sdX mounted raw images for its VMs' hard drives.

We prefer using VMDK solely because this format most frequently has the most helpful resources online.

Process
-------------------------------------------------------------------

Get the OVA file onto the Proxmox server itself and place it in the `/root` directory. Depending on the size of the OVA, I've been able to SCP the file over to `/root` on the hypervisor or to mount a USB drive with the OVA on it.

Examples:

```
root@proxmox:~# scp <user>@<IpOfSysWithOva>:/path/to/file.ova /root/file.ova

-OR-

  [[Insert USB drive with OVA file.]]
root@proxmox:~# fdisk -l 
  [[Identify device name for USB drive volume with OVA file.]]
root@proxmox:~# mkdir /root/extusb
root@proxmox:~# mount </dev/sdX> /root/extusb
root@proxmox:~# cp /root/extusb/file.ova /root/file.ova
```

Extract OVA file.

```
root@proxmox:~# tar -xvf file.ova
```

Gather VM system requirements to build a VM to spec in Proxmox. 

```
root@proxmox:~# cat file.ovf
  [[Identify quantity of cores and memory.]]
root@proxmox:~# qemu-img info file.vmdk
  [[Identify virtual disk size.]]
```

Create a new VM in Proxmox GUI and match or exceed image hardware requirements. **Select “Do not use any media” in the CD/DVD tab and IDE as the Bus/Device in the Hard Disk tab.**

Convert the .vmdk virtual hard disk file to .raw format.

```
root@proxmox:~# qemu-img convert file.vmdk -O raw file.raw
```

Clone the .raw file into the newly created logical volume located at /dev/pve/. You are essentially overwriting the empty virtual hard drive of the newly-created VM with the contents of the VM contained in the OVA.

```
# dd if=/root/file.raw of=/dev/pve/<vm-100-disk-1> bs=1M
```

Lastly, fire up the VM and ensure it works!
