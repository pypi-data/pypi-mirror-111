# What the hell is this?

Tourbox is a small usb device by Tourbox Tech Inc. Which lets you assign custom program actions and hotkeys.
This Python script translates the serial IO to an evdev/uinput device.

## Install

    sudo pip install git+https://github.com/bloodywing/tourboxneo
it needs to install a udev rule.

## Last words

This was hacked together in one day, the wrapper is far from perfect. But at least it makes it possible to use that
expensive device with Linux
