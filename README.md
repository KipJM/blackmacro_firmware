# Blackmacro Keyboard Firmware
Firmware for the open-source [Blackmacro video editing & macropad keyboard](https://github.com/KipJM/blackmacro-hardware),
written in Micropython.

**This firmware is designed for the Blackmacro V2 and is incompatible with Blackmacro V1.**

For more information, see:
- ### **Blackmacro hardware: https://github.com/KipJM/blackmacro-hardware**
- Blackmacro reference lib: https://github.com/KipJM/blackmacro-lib

# License
> The Blackmacro firmware (not to be confused with the Blackmacro-lib reference firmware) is currently **NOT released under
> any open-source license**. I, KIP, am the sole author of this project and retains all of its copyright. This project is
> comes with absolutely no warranty and is currently "source-available". You are allowed to use or modify this project
> for personal use, but you're **strictly forbidden** from distributing, selling, or claiming authorship over this project
> or its modified versions. 

You're also strictly forbidden from using this project to train "Generative AI" analytical machine learning models (e.g. LLMs).

The firmware is currently "source available", but not under any open-source license. When I feel the project's 
mature enough to receive contributions, I may switch it to a strong copyleft license like AGPLv3.
For now, **All Rights Reserved**.

# Running
I currently do not provide precompiled .uf2 images for this project. If you have a blackmacro v2 keyboard, do this:
- Flash the latest micropython firmware onto the pico.
- Connect your computer to the pico's REPL over usb.
- Copy everything from this project's pico folder into the pico's filesystem.
- Power cycle the keyboard.

Beware that the project is still in development and is unstable.

# Davinci Resolve Support
This firmware includes native compatibility with the Davinci Resolve video editing software. For more information on how
this is achieved, see https://github.com/KipJM/blackmacro-lib.

---

# Known Issues:
This firmware is designed to run with seamless transition between usb and battery power. However if debug prints are turned on,
directly disconnecting the USB cable while a serial REPL is still connected will cause the firmware to hang.

# TODO:
- Screen display & GUI
- Motor control

