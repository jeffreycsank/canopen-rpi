About
==========

This repository actually contains two programs that complement each other, but can be used independently.  The first is a CAN-to-HTTP webserver (`canhttp.py`) that translates CAN bus messages to a `text/event-stream`, and `HTTP GET` or `POST` requests into CAN bus messages.  The second is a CANopen Master node (`canopen-master.py`) that acts as a SYNC producer and Heartbeat consumer.  The code supports up to two CAN busses, and if only one is used, some minor modifications are necessary.

Raspberry Pi Setup
==================

Install and Configure Raspbian
------------------------------


1. Install the latest version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/).

2. (Optional) Run `sudo raspi-config` and adjust internationalization options.

3. (Optional) Prevent flash memory corruption:

    1. Change `/etc/fstab` to:

        ```
proc            /proc     proc    defaults          0   0
/dev/mmcblk0p1  /boot     vfat    ro,noatime        0   2
/dev/mmcblk0p2  /         ext4    defaults,noatime  0   1
none            /var/log  tmpfs   size=1M,noatime   0   0
        ```

    2. Disable swap memory:

        ```
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove
        ```

    3. Reboot: `sudo reboot`

Internet Connection
-------------------
An internet connection to the Raspberry Pi is required to install software not included in the base image.  With some WiFi adapters, you may need to do the following:
1. Adjust power driver settings.
Add `8192cu.conf` file
```
sudo nano /etc/modprobe.d/8192cu.conf
```
Then add the single line
```
options 8192cu rtw_power_mgnt=0 rtw_enusbss=0
```
This will disable power management for 8192cu driver

1. Configure wireless adapter and connect to nasaguest (required after each power-on)
```
sudo iwconfig wlan0 essid <WIFI_SSID>
sudo dhclient wlan0
````

2. If not using DHCP, set static IP address in `/etc/dhcpcd.conf`:

    ```
interface eth0
static ip_address=x.x.x.x/24
    ```

Add CAN Support
-----------------------------

1. If necessary, enable writable boot partition: `sudo mount -o remount,rw /dev/mmcblk0p1 /boot`

1. Run `sudo raspi-config`
    * Advanced Options
        * A6 SPI: Enable and load it by default at boot

2. Configure SPI Module: Change `/boot/config.txt` to:

    ```
dtparam=spi=on
dtoverlay=mcp2515-can0-overlay,oscillator=16000000,interrupt=25
dtoverlay=mcp2515-can1-overlay,oscillator=16000000,interrupt=24
dtoverlay=spi-bcm2835-overlay
    ```

3. Setup CAN interfaces
    * Manual

    ```
sudo ip link set can0 up type can bitrate 1000000
sudo ip link set can1 up type can bitrate 1000000
    ```
    * Automatic (start at boot-up)
        * Copy `can_if` to `/etc/init.d/` *(modified from [linux-can/can-misc](/linux-can/can-misc/blob/master/etc/can_if))*
        * `sudo update-rc.d can_if defaults`
        * `sudo reboot` or `sudo /etc/init.d/can_if start`

4. (Optional) Install `can-utils` for debugging

    ```
sudo apt-get install can-utils
    ```

Configure as CANopen Master
----------------------------

5. Install `python3-rpi.gpio`

    ```
sudo apt-get install python3-rpi.gpio
    ````

8. Setup webserver
    * Copy contents of [GUI](/bggardne/AMPS-MoSS/tree/master/GUI) directory to `/home/pi/`
    * Copy [canhttp.py](/bggardne/AMPS-MoSS/blob/master/RPi/canhttp.py) to `/home/pi/`
    * Copy [canhttp](/bggardne/AMPS-MoSS/blob/master/RPi/canhttp) to `/etc/init.d/`
    * `sudo update-rc.d canhttp defaults`
    * Copy [canopen-master.py](/bggardne/AMPS-MoSS/blob/master/RPi/canopen-master.py) to `/home/pi/`
    * Copy [canopen-master](/bggardne/AMPS-MoSS/blob/master/RPi/canopen-master) to `/etc/init.d/`
    * `sudo update-rc.d canopen-master defaults`

9. Reboot: `sudo reboot`
