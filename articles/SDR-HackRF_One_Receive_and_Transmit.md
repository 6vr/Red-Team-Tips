HackRF One Receive and Transmit
===============================

Many of the HackRF's uses require recording and broadcasting radio streams. These streams are raw data entering or leaving the HackRF, but they're similar in nature to WAV audio files. Signal analysis is covered in the section "Spectrum Analyzer Crash Course". Demodulating signals is covered in the section "Demodulating Radio Signals".

*Note*: This section assumes your HackRF One and host computer have been prepared and configured according to the section "Spectrum Analyzer Crash Course". If that isn't true for you, then complete "Installation & Configuration" in that section before proceeding.



Receiving
---------

Both receiving and transmitting use the `hackrf_transfer` tool on the host computer. You'll usually want to record whichever signal you receive, and that's quite simple. It does, however, involve two caveats:

1. First, you obviously have to identify the signal you want and its center frequency. More complex signals require additional parameters that you'll learn through OJT or office-hours sessions. 

2. Second, you need to include an offset from the center frequency for recording. This is due to DC bias, or how the SDR hardware amplifies its signals. Unfortunately, the center-tuned frequency basically shows erroneous constant received signal, which tends to override the modulated signal itself. You could ignore the offset if analyzing the signal visually, but it will hinder replay attempts later.

In this example, we will record a North American-region car keyfob, which operates at 315 MHz. (FCC documentation confirms operation at exactly 315 MHz. As a function-check, my HackRF One was tuned adequately enough that spectrum analysis revealed the keyfob operating at 315 MHz on my display.) These steps are performed rapidly, with only 3-5 seconds of recording received signals. 5 seconds tends to yield recorded filesizes of 80-100 MB, although that varies widely depending on protocol, bandwidth, and sample rate.

***DC Bias Correction***: A quick word about the tuned frequency. As caveat #2 (above) mentioned, it is rarely advisable to record directly on the desired frequency. In the command below, I record on 315.020 MHz, or 20 kHz above the target frequency.

### Process

Start recording:

```
$ hackrf_transfer -r keyfobunlock.wav -f 315020000
```

Press keyfob unlock button several times. Only take a few seconds to do this, or your output file will be huge.

Stop recording by typing `[CTRL]+[C]`.

### What This Does

It records the signals transmitted by your keyfob on 315 MHz as raw data into the file `keyfobunlock.wav`.



Transmitting
------------

You can transmit any data recording you have. In this example, we'll just transmit the keyfob unlock signals we recorded above. (This is actually a keyfob replay attack against the vehicle and works with older model cars that lack time-variable encoding mechanisms.)

```
$ hackrf_transfer -t keyfobunlock.wav -f 315200000 -x 20
```

The variable above is the output power, measured in gain: `-x 20`. This is a reasonable value for a low-power device. Higher values (40+) could potentially be used to jam a targeted receiver by overpowering the signal it is intended to receive. I haven't tested output settings and their efficacy with respect to Jam/Signal ratio, nor have I evaluated bandwidth spread at higher output powers. Conceivably, one could record different noise and signal patterns and jam by transmitting different recorded data files against target receivers.


