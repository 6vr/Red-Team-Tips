Spectrum Analyzer Crash Course
==============================

Everything should be: quick, easy, and cheap.

-**Quick**: This guide provides all necessary settings to get you up and running quickly.

-**Easy**: Required equipment is very portable and installs from package manager repositories.

-**Cheap**: You need a laptop running Linux, a HackRF One, and several no-cost, open-source tools.

I use Q Spectrum Analyzer on Linux as my variable-width spectrum analyzer. While the data are somewhat messy and imprecise at extended spectrum views, this tool enables viewing the entire spectrum range of the HackRF One, from below 1 MHz through 6 GHz, at a single time. Each spectrum analysis application (e.g., SDR#, GQRX, HackRF Sweep Spectrum Analyzer, RF Analyzer) has its own automatic filter and gain adjustments and quirks. This entire article only covers Q Spectrum Analyzer since it suits our needs quite well and provides the most detailed output of certain common target frequencies.

<br>

Installation & Configuration
----------------------------

**Required to begin this process**:
- x86_64 computer with minimum 2x USB 2.0 ports
- HackRF One with any omni-directional SMA antenna
- Internet connection during configuration

<br>

### STEP 1: Operating System

Install Linux Mint onto your computer. I used version 18.3 "Sylvia" with XFCE desktop environment. For international travel, I recommend using full-disk encryption with a complex passphrase. You will run your spectrum analyzer as the default account you create during installation.

<br>

### STEP 2: HackRF One Host Tools

Install latest HackRF tools for your computer.

```
$ sudo apt install hackrf
```

<br>

### STEP 3: HackRF One Device Firmware

Connect your HackRF One to your computer. Ensure it is recognized by your computer (see output of command).

```
$ hackrf_info 
hackrf_info version: unknown
libhackrf version: unknown (0.5)
Found HackRF
Index: 0
Serial number: 0000000000000000a06063c82231265f
Board ID Number: 2 (HackRF One)
Firmware Version: 2018.01.1 (API:1.02)
Part ID Number: 0xa000cb3c 0x00684f5b
```

Download the latest firmware bundle. Get the latest bundle [here](https://github.com/mossmann/hackrf/releases).

Navigate to the downloaded file and decompress it.

```
$ cd ~/Downloads/
$ tar xvf hackrf-2018.01.1.tar.xz 
```

Upgrade the firmware on your HackRF One device.

```
$ cd ~/Downloads/hackrf-2018.01.1/
$ hackrf_spiflash -w firmware-bin/hackrf_one_usb.bin
$ hackrf_cpldjtag -x firmware/cpld//sgpio_if/default.xsvf 
```

*IMPORTANT*: Unplug your HackRF One. Plug it back in. This resets it.

<br>

### STEP 4: Q Spectrum Analyzer

If you run into trouble, [this page](https://github.com/xmikos/qspectrumanalyzer) covers installation for Ubuntu and Ubuntu-derivatives (e.g., Linux Mint). I recommend you just follow the instructions I used below.

```
sudo add-apt-repository -y ppa:myriadrf/drivers
sudo apt update
sudo apt-get install python3-pip python3-pyqt5 python3-numpy python3-scipy soapysdr python3-soapysdr
sudo apt-get install soapysdr-module-rtlsdr soapysdr-module-airspy soapysdr-module-hackrf soapysdr-module-lms7
pip3 install --user setuptools
pip3 install --user wheel
pip3 install --user qspectrumanalyzer
```

<br>

Usage
-----

I recommend breezing through the "Signal Identification" and "Practice" subsections below before proceeding. Don't worry about absorbing any of the content yet, but you'll want to get a grasp on the overall process of analysis before attempting meaningful use of your spectrum analyzer. This will prevent much frustration.

<br>

### STEP 1: Open the App

Open Q Spectrum Analyzer by typing `[ALT]+[F2]`, entering `qspectrumanalyzer`, and hitting `[ENTER]`. The application's GUI will open.

<br>

### STEP 2: Choose Backend

From the drop-down menu, select `File` > `Settings`. Choose your backend. You will have to do this at the start of each session and any time you want to change backends. ("Backend" is just the developer's term for which SDR software your host computer will run for the spectrum scan.) You should only select one of two options at this point: `soapy_power` and `hackrf_sweep`. General guidance for which backend to use based on viewable spectrum is:

- *Narrower than 100 MHz* - If you want to view up to 100 MHz of spectrum at a time, use `soapy_power`. This backend operates the HackRF One in a conventional manner. An example scan range would be 400-500 MHz.

- *100 MHz - 1 GHz* - In this intermediate range, rely on experience (practice) to determine which backend to use.

- *Wider than 1 GHz* - Viewing 1 GHz or more of spectrum at a time works best when using HackRF One's `hackrf_sweep` function, so choose that as the backend. In this mode, the HackRF One will repeatedly retune itself at intervals through your spectrum view multiple times a second to achieve the continuous spectrum view you desire.

Once you choose the backend, accept the settings and close the settings window.

<br>

### STEP 3: Settings

The right panel contains various settings. Some, such as `Start` and `Stop` within the `Frequency` section are obvious. Others require some experience to set properly. The settings shown in STEP 4: Capture (below) will get you started. Adjust off the examples to achieve your desired views. I omit `Corr.`, `Crop`, and any checkboxes that are deselected. I include the associated backend for which these settings apply. 

<br>

### STEP 4: Capture

This one is easy. Hit `Start` to begin capture and `Stop` to end capture. Anytime you adjust the settings, stop and restart capture. This clears the display and, more importantly, resets the HackRF One. Sometimes incorrect input or Murphy's Law cause your HackRF One to freeze. Just hit the reset button on the device or unplug it and plug it back in to reset it. Some configurations, particularly those using the `soapy_power` backend across wide views, take up to 20 seconds to display output on the screen.

For simplicity's sake, I've included everything from STEP 3 and this step below. I lay out in text the settings that you input before hitting `Start` and follow that with a screenshot that shows both the settings and the displayed output resulting from those settings after hitting `Start`.

<br>

#### Very Wide View

- *Backend: hackrf_sweep*
- Start: 1.000 MHz
- Stop:  6,000.000 MHz
- Bin size: 100.000 kHz
- Interval: 0.00 s
- Gain: 40 dB
- Checked boxes: Max hold, Average, Smoothing

What you get:

![alt text](data/1M-6G.png "1 MHz - 6 GHz view")

<br>

#### 1 GHz View (hackrf_sweep)

- *Backend: hackrf_sweep*
- Start: 2,000.000 MHz
- Stop:  3,000.000 MHz
- Bin size: 40.000 kHz
- Interval: 0.00 s
- Gain: 40 dB
- Checked boxes: Max hold, Smoothing

What you get:

![alt text](data/1G_hackrf_sweep.png "1 GHz view with hackrf_sweep")

<br>

#### 1 GHz View (soapy_power) (very slow)

- *Backend: soapy_power*
- Start: 2,000.000 MHz
- Stop:  3,000.000 MHz
- Bin size: 100.000 kHz
- Interval: 0.01 s
- Gain: 37 dB
- Checked boxes: Max hold, Smoothing

What you get:

![alt text](data/1G_soapy_power.png "1 GHz view with soapy_power")

<br>

#### 300-MHz View (slow)

- *Backend: soapy_power*
- Start: 2,300.000 MHz
- Stop:  2,600.000 MHz
- Bin size: 10.000 kHz
- Interval: 0.01 s
- Gain: 37 dB
- Checked boxes: Max hold, Smoothing

What you get:

![alt text](data/300M.png "300 MHz view")

<br>

#### 100-MHz View Signal Peaks

- *Backend: soapy_power*
- Start: 2,380.000 MHz
- Stop:  2,480.000 MHz
- Bin size: 1.000 kHz
- Interval: 0.01 s
- Gain: 37 dB
- Checked boxes: Max hold, Smoothing

What you get:

![alt text](data/100M-peaks.png "100 MHz view of seen signals")

<br>

#### 100-MHz View Realtime Signals 1

- *Backend: soapy_power*
- Start: 2,380.000 MHz
- Stop:  2,480.000 MHz
- Bin size: 1.000 kHz
- Interval: 0.01 s
- Gain: 37 dB
- Checked boxes: Main curve, Smoothing

What you get:

![alt text](data/100M-realtime1.png "100 MHz view 1")

<br>

#### 100-MHz View Realtime Signals 2

- *Backend: soapy_power*
- Start: 2,380.000 MHz
- Stop:  2,480.000 MHz
- Bin size: 1.000 kHz
- Interval: 0.01 s
- Gain: 37 dB
- Checked boxes: Smoothing, Persistence

What you get:

![alt text](data/100M-realtime2.png "100 MHz view 2")

<br>

#### 200-MHz View Realtime Signals

- *Backend: soapy_power*
- Start: 1,700.000 MHz
- Stop:  1,900.000 MHz
- Bin size: 5.000 kHz
- Interval: 0.01 s
- Gain: 37 dB
- Checked boxes: Max hold, Smoothing, Persistence

What you get:

![alt text](data/200M-realtime.png "200 MHz view with one transmitter turned off")

<br>

Signal Identification
---------------------

Much of spectrum analysis is based on experience with specific protocols and target transmitters. Nevertheless, the basics still apply: within a single protocol, closer transmitters show up with greater amplitude. (Different protocols and devices will have different ERPs, however, so just because you see something as quiet doesn't mean it's necessarily far away.)

Here I present an example basic analysis with the available hardware (HackRF One). I only use signal strength as the indicator of a threat frequency in the example, but that doesn't mean most threats are detected this way. To the contrary, actually--a target list of commonly-used threat frequencies is most common (and most helpful). That way, you know which frequencies to scan for immediately and can confirm or deny the presence of such emitters. After the targeted, aka "informed" scan of known threat frequencies, you should still follow up with a scan such as in the example below and a baseline for that physical area. 

<br>

### Example: Two different transmitters

I begin with a wide scan of about 1 GHz using the `hackrf_sweep` backend. This scan took about 15 seconds.

![alt text](data/example-1G.png "Example - 1 GHz scan")

Right off the bat, I'm concerned with the two tall peaks on either side of 1.8 GHz. They are of relatively high power, which makes me think they are close. Furthermore, they don't appear to occupy populated channels, which makes it likely that they are not conventional transmitters. Of note, `hackrf_sweep` tends to show an accurate noise floor, which here is only elevated around 3 dB above -72 dB. One signal is at -48 dB, and the other is at -44 dB. In comparison, the other signals I see around 1.3 GHz (which appear to occupy channels) are at a high-end average of -58 db, or 10 times quieter than the weaker of the two target signals.

I definitely want to analyze these more closely, so I'll use `soapy_power` to look at 1.7 GHz through 1.9 GHz. I only this scan run for 10 seconds before deciding I could zoom further in. (`soapy_power` is slow at or above 200 MHz, so it makes for painful realtime views. In reality, I'd probably isolate each signal for individual viewing to avoid this slow view, but it works well for the example.)

![alt text](data/example-200M.png "Example - 200 MHz scan")

Let's zoom in to 1.75 through 1.85 GHz. Note that I reduce the bin size to achieve better resolution. Here I'll have a good view of each signal's spread. I'll want to characterize these signals better, so I let this run for a minute.

![alt text](data/example-100M.png "Example - 100 MHz scan")

Now I'm getting somewhere. The red line in the above screenshot is Max hold, or the peak signal strength observed. The other line is the average signal strength seen. I can deduce from the large vertical gap between the two lines in the lefthand signal that the upper portion of its transmissions are variable or bursting. I can also tell by the lefthand signal's shape (solidly-occupied bandwidth with vertical sides) that it is a digital signal modulated to occupy a spread of spectrum. In comparison, the signal on the right hand appears analog based on its sloping or curved sides.

(Unfortunately, the received signal strength axis appears incorrectly incremented with dB. I will try to fix this for future `soapy_power` use.)

At this point, I would begin (1) trying to direction-find the transmitters to assess with more confidence whether they are threats and (2) more precisely characterizing them.

<br>

### Other Signals

My goal here is to provide visual display examples of various protocols of signals, at different spectrum zooms. This will obviously take time and require that I locate the relevant emitters.



<br>

Practice
--------

As stated above, the best way to use these tools effectively (and to develop your own tools and methods) is Practice, Practice, Practice! But how do you go about practicing analysis of signals that might not exist in your environment--or signals that do exist, but in overlapping, dirty configurations? The best answer is to generate your own signals with some known parameters. This builds confidence in the equipment and allows you to calibrate the equipment or software if necessary. It also makes for easy demos.

Good emitters for practice won't compete with environmental signals for bandwidth (unless you're specifically training on extracting target signals from popularly-used channels). We start with the two emitters seen in the "Signal Identification" subsection's example. Most people in our specific field have access to these emitters and should be able to perform this training. Furthermore, by owning the specific emitter, you already know its characteristics and can turn it off to confirm you have found the right one.

Ideal emitters have frequency and power adjustments so you can actually train on hunting them. For burst and spread spectrum emitters, adjusting the bursting and hopping algorithms is certainly helpful. These additional traits would enable a trainee to enter a black-box room or environment and detect, identify, characterize, and locate the threat transmitters. Black-box training with feedback is supreme.











