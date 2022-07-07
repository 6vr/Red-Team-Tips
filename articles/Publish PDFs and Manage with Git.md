Publish PDFs and Manage with Git
================================================================================

A workflow to publish markdown projects to PDF and sync on Github.

Gitbook is a tool (and an online service, but I just use the standalone tool) that creates HTML, ePub, and PDF books from markdown files.

I'm already a fan of markdown for its rendering simplicity and legibility on a CLI, and gitbook makes it easy to convert markdown into a final-rendered PDF. As its name implies, gitbook also works well with git. I tend to maintain all my documentation repos on github, and I even push to my online repos certain gitbook-related files: a SUMMARY.md file, a cover.jpg file, and the published PDF. Even with the binary picture files and PDFs, pushing to my online repos is a snap. The benefit is that I always have the most recent version of the document in question (ex: an exploit manual) and can use git's organic branches to develop new versions.

Prepare system with required applications
--------------------------------------------------------------------------------

This installs RVM, Ruby 2.3, npm, and gitbook-cli. Obviously, you only do this once for each system.

```
user@SpFx:~$ \curl -sSL https://get.rvm.io | bash -s stable --ruby

user@SpFx:~$ rvm install ruby-2.3

user@SpFx:~$ ruby -v
  ruby 2.3.4p301 (2017-03-30 revision 58214) [x86_64-darwin16]

user@SpFx:~$ brew install npm

user@SpFx:~$ npm install -g gitbook-cli
```

Write and organize your book
--------------------------------------------------------------------------------

### Create your markdown file collection

In other words, create your content. It doesn't have to be in specific order, but consider the transformations that will occur later:

- Every markdown file becomes its own section/chapter/page/article in the published PDF.
- Directories are immaterial in my workflow, so feel free to lump photos into a separated directory than markdown files, for example.

Your repo's content will look much like this:

```
user@SpFx:/PathOmitted/UserGuide$ ls *.md | grep -v SUMMARY
Field-Charging.md
Field-During Event.md
Field-Event End.md
Field-Event Start.md
Field-Placement.md
Field-Pre-Event Inspection.md
README.md
Remote-Capturing and Correlating Requests.md
Remote-End Event Support.md
Remote-Managing and Reconnecting to tmux Sessions.md
Remote-Overview.md
Remote-Pre Event Inspection.md
```

### Organize everything with SUMMARY.md

You'll define chapters (or major sections) in SUMMARY.md, a separate file used just by gitbook. While you could automate this file's construction based on the repo's component files, I find it more useful to construct SUMMARY.md as I go, using it as a virtual outline while I write my content. I comment-out planned sections that have to wait for a future release.

This is an example of a different project's SUMMARY.md. Here you'll notice all the content is inside a directory named "Sections". This is simply for your own ease of organization and isn't recommended for small projects. Again, for this workflow I prefer to add the next section to the SUMMARY.md file, commented out (so I don't forget that I need to finish it), and then write the markdown file itself. Once I've written it, I uncomment the line in SUMMARY.md and execute the PDF construction process.

```
# Summary

* [Introduction](README.md)

* Sections

  * [Anatomy of an Attack](Sections/Anatomy of an Attack.md)
  * [C Refresher](Sections/C Refresher.md)
  * [Enable Monitor Mode on Macbook Pro](Sections/Enable Monitor Mode on Macbook Pro.md)
  * [Identify and Enumerate SNMP Targets](Sections/Identify and Enumerate SNMP Targets.md)
  * [Import OVA Virtual Appliance into Proxmox](Sections/Import OVA Virtual Appliance into Proxmox.md)
  * [Java Signed Applet Attack](Sections/Java Signed Applet Attack.md)
  * [KPi on Raspberry Pi Zero W](Sections/KPi on Raspberry Pi Zero W.md)
  * [Kali Tools](Sections/Kali Tools.md)
  * [Make a 32-bit Kali live USB with encrypted persistence](Sections/Make a 32-bit Kali live USB with encrypted persistence.md)
  * [Manufacturer BIOS and UEFI Master Passwords](Sections/Manufacturer BIOS and UEFI Master Passwords.md)
  * [Markdown Cheatsheet](Sections/Markdown Cheatsheet.md)
  * [Markdown Software](Sections/Markdown Software.md)
  * [Metasploit](Sections/Metasploit.md)
  * [More Resources](Sections/More Resources.md)
  * [Persistent Reverse AutoSSH Connections](Sections/Persistent Reverse AutoSSH Connections.md)
  * [SQL Injection Basics](Sections/SQL Injection Basics.md)
  * [Simple Buffer Overflow Attack](Sections/Simple Buffer Overflow Attack.md)
  * [Targeting Web Browsers without BeEF](Sections/Targeting Web Browsers without BeEF.md)
  * [Uploading Tools to Windows](Sections/Uploading Tools to Windows.md)
  * [Windows Post-Exploitation](Sections/Windows Post-Exploitation.md)
  * [Windows Tools](Sections/Windows Tools.md)
```

Add a cover to your book
--------------------------------------------------------------------------------

You don't have to follow this exactly--you just need a file named `cover.jpg` in the root of your repo for gitbook to ingest it automatically. But, I use this workflow.

Create a Powerpoint presentation named `cover.pptx` and save it in the root directory of your repo. Change the slide dimensions to portrait-oriented US Letter size (8 1/2 inches wide by 11 inches tall).

Copy and paste whatever graphics you want. Then add text, such as your title, date published, your name, etc. Use <kbd>ctrl</kbd> + <kbd>A</kbd> or <kbd>cmd</kbd> + <kbd>A</kbd> on a Mac to select all the elements on the slide. Right-click and select `Save as Picture...`. Save the <i>picture</i> in JPEG format and to filename `cover.jpg` in your repo's root directory.

If you publish a new version, just update the text in the Powerpoint file and repeat saving as cover.jpg. If you have to clone the repo from Github, it'll clone `cover.pptx` along with all your other files.

Publish locally
--------------------------------------------------------------------------------

We'll finally use gitbook to generate the PDF. This is the easy part.

```
user@SpFx:/PathOmitted/UserGuide$ gitbook build .
user@SpFx:/PathOmitted/UserGuide$ gitbook pdf . "<title>.pdf"
user@SpFx:/PathOmitted/UserGuide$ rm -rf _book
```

Here's the output. Note the PDF file at the end.

```
user@SpFx:/Volumes/SyncPart/Sync/Repos/CellRAT-UserGuide$ gitbook build .
info: 7 plugins are installed
info: 6 explicitly listed
info: loading plugin "highlight"... OK
info: loading plugin "search"... OK
info: loading plugin "lunr"... OK
info: loading plugin "sharing"... OK
info: loading plugin "fontsettings"... OK
info: loading plugin "theme-default"... OK
info: found 13 pages
info: found 19 asset files
info: >> generation finished with success in 3.2s !

user@SpFx:/Volumes/SyncPart/Sync/Repos/CellRAT-UserGuide$ gitbook pdf . "CellRAT User Manual v2018-02-12.pdf"
info: 7 plugins are installed
info: 6 explicitly listed
info: loading plugin "highlight"... OK
info: loading plugin "search"... OK
info: loading plugin "lunr"... OK
info: loading plugin "sharing"... OK
info: loading plugin "fontsettings"... OK
info: loading plugin "theme-default"... OK
info: found 13 pages
info: found 19 asset files
info: >> generation finished with success in 7.3s !
info: >> 1 file(s) generated

user@SpFx:/Volumes/SyncPart/Sync/Repos/CellRAT-UserGuide$ rm -rf _book

user@SpFx:/Volumes/SyncPart/Sync/Repos/CellRAT-UserGuide$ ls
CellRAT User Manual v2018-02-12.pdf                  Remote-End Mission Support.md
Field-Charging.md                                    Remote-Exploit WiFi Networks on Objective.md
Field-During Mission.md                              Remote-Managing and Reconnecting to tmux Sessions.md
Field-Mission End.md                                 Remote-Overview.md
Field-Mission Start.md                               Remote-Pre-mission Inspection.md
Field-Placement.md                                   SUMMARY.md
Field-Pre-Mission Inspection.md                      cover.jpg
README.md                                            images
Remote-Capturing and Correlating Probe Requests.md   publish.sh

```

Push to Github repo for public consumption
--------------------------------------------------------------------------------

Use whatever method you prefer to `commit` these changes and `push` them to your online repo.

Note that you're pushing all content, all organization files, and the Powerpoint cover construction file. All you have to do for new releases is add to what's already there. Also note that you're pushing the PDF itself. Why not? Then you have everything in one place.

For an example of one of these projects, check out my repo [Life-After-Watson](https://github.com/viiateix/life-after-watson).

