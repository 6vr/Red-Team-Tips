Markdown Software
================================================================================

*Note: This article assumes you have `git` installed on your system. If not, follow the following instructions for Linux or modify appropriately for Mac or Windows. Not all methods require `git`, so feel free to skip this if you want.*

```
$ sudo apt update
$ sudo apt install git
```

Viewing Markdown Documents (Such as These Articles)
--------------------------------------------------------------------------------

### [1] From a web browser

This works on any device and displays rendered markdown. Browse [this repo](https://github.com/viiateix/Life-After-Watson) in any web browser. Done.

### [2] On the CLI

Clone this repo and then view the articles with `cat`, `more`, `vim`, or a GUI text editor. Obviously, you'll be seeing the markdown without rendering, so in plaintext. But it's still useful at times on remote machines...if you don't have your own connection or can't copy and paste (such as through a VNC session).

```
$ mkdir ~/Repos           # <--- Or put this wherever you want
$ cd ~/Repos
$ git clone https://github.com/viiateix/Life-After-Watson.git
$ cd Life-After-Watson
$ cd Articles
$ more <article name>.md
```

### [3] On a mobile device

One of the most convenient ways to view this repo is on your phone. I don't currently have an app picked for Android devices, but I recommend CodeHub for iPhone. You'll have to navigate to the repo (you can pin it for future quick access) and then scroll down to "Source Code". From there, it's similar to viewing rendered markdown files on Github.

### [4] In a markdown editor

I cover this in the "Editing Markdown Documents" section below. If you're going to write notes to contribute to this or other markdown-based repos, you'll need an editor and probably end up viewing markdown files in the editor for convenience.


Editing Markdown Documents
--------------------------------------------------------------------------------

### [1] On a Mac

I use MacDown for macOS. It's relatively simple. Each file opens a new window that mainly consists of a plaintext editing pane on the left and a real-time, rendered preview pane on the right.

### [2] On Debian variants of Linux

I use Remarkable from https://remarkableapp.github.io/linux.html. Works well for me so far.

