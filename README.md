About
==========

This repository actually contains two programs that complement each other, but can be used independently.  The first is a CANopen Master node (`canopen-master.py`) that acts as a SYNC producer, Heartbeat consumer, and EMCY producer.  The second is a CAN-to-HTTP webserver (`canhttp.py`) that translates CAN bus messages to a `text/event-stream`, and `HTTP GET` or `POST` requests into CAN bus messages.  The code supports up to two CAN busses, and if only one is used, some minor modifications are necessary.

Raspberry Pi Setup
==================

Install and Configure Raspbian
------------------------------


1. Install the latest version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/).

2. (Optional) Because of a [driver issue](https://github.com/raspberrypi/linux/issues/1317), you may need to add `dtoverlay=mmc` to `/boot/config.txt` for the Raspberry Pi to boot.

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

* Configure wireless adapter and connect to nasaguest (required after each power-on)

    ```
sudo iwconfig wlan0 essid <WIFI_SSID>
sudo dhclient wlan0
    ```

* If not using DHCP, set static IP address in `/etc/dhcpcd.conf`:

    ```
interface eth0
static ip_address=x.x.x.x/24
    ```

Add CAN Support
-----------------------------

1. Connect MCP2515 circuit(s) to the Raspberry Pi `SPI0` bus.  Interrupt GPIOs are defined in step 4.

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
    *Note: The `oscillator` and `interrupt` parameters may be different for your application.*

3. Setup CAN interfaces
    * Manual

    ```
sudo ip link set can0 up type can bitrate 1000000
sudo ip link set can1 up type can bitrate 1000000
    ```
    * Automatic (start at boot-up)
        * Copy [can_if](https://github.com/linux-can/can-misc/blob/master/etc/can_if) to `/etc/init.d/`
        * Modify `can_if` line `CAN_IF=""` to `CAN_IF="can0@1000000,500 can1@1000000,500"` *(may vary per application)*
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
    * Copy contents of [GUI](/GUI) directory to `/home/pi/`
    * Copy [canhttp.py](/canhttp.py) to `/home/pi/`
    * Copy [canhttp](/canhttp) to `/etc/init.d/`
    * `sudo update-rc.d canhttp defaults`
    * Copy [canopen-master.py](/canopen-master.py) to `/home/pi/`
    * Copy [canopen-master](/canopen-master) to `/etc/init.d/`
    * `sudo update-rc.d canopen-master defaults`

9. Reboot: `sudo reboot`

HTTP to CAN API
========================
* The HTTP to CAN API uses the HTTP/1.1 protocol's GET method.
* Telemetry responses use the [server-side event API](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)

Telemetry
---------
When the host URL is accessed without query string parameters, a `text/event-stream` is opened and CAN traffic is streamed as JSON-encoded data-only events.  The JSON objects shall have the following attribute-value pairs:
* `bus`: Which CAN bus message was received (if multiple; 0 or 1 e.g.)
* `id`: 11-bit CAN identifier, in base 10
* `data`: Array of CAN data bytes (0-8 bytes), in base 10
* `ts`: ISO 8601 time-stamp of when the CAN message was received

*Note: This assumes the events can be supplied faster than CAN frames are received.  It is suggested that CAN frames be buffered, and an `error` event sent if the buffer overflows (see Errors section).*

**Example**

Request: `GET / HTTP/1.1`

Response: (one data-only event per CAN frame)
```
HTTP/1.1 200 OK
Access-Control-Origin: *
Content-Type: text/event-stream
Cache-Control: no-cache

data:{"bus": 0, "id": 123, "data":[255,128,5], "ts":"2015-12-21T10:36:30.123Z"}

data:{"bus": 1, "id": 157, "data":[], "ts":"2015-12-21T10:36:56.789Z"}
```

Commands
--------
When the host URL is accessed with a valid set of query string arguments listed below, the command is translated to a CAN frame.
* `id`: (required) The 11-bit CAN identifier, in base 10
* `data`: (optional) A JSON-encoded array of CAN data bytes (in base 10), having a length of 0-8.

**Example**

Request: `GET /?id=123&data=[255,128,5] HTTP/1.1`

Response:
```
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: *

```

Errors
======

If no query string is present, and the state of the CAN bus (or busses) are abnormal, an `error` event is streamed (once) if "bus-off" or a `warning` event if "error warning" (error count exceeds a threshold).  A `notice` event is streamed if the bus (or busses) return to a normal state.

**Example**

Request: `GET / HTTP/1.1`

Response:
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: text/event-stream
Cache-Control: no-cache

event: error
data: Bus 0 is in the bus-off state

event: warning
data: Bus 1 is in the warning state

event: notice
data: Bus 1 is now in a normal state

event: error
data: CAN RX buffer overflow on bus 1

```

If a query string is present, but the required command parameters do not exist or are invalid, then an HTTP 400 code shall be returned.  All other errors shall be formatted per the [JSON API](http://jsonapi.org/format/#error-objects).


**Example**

Request:

`GET /?badargument=1 HTTP/1.1` or

`GET /?id=4096&data=[] HTTP/1.1` (invalid id) or

`GET /?id=123&data=[256] HTTP/1.1` (invalid data byte) or

`GET /?id=123&data=[0,0,0,0,0,0,0,0,0]` (too many data bytes)

Response:
```
HTTP/1.1 400 Bad Request
Access-Control-Allow-Origin: *

```

**Example**

Request `GET /?id=123&data[] HTTP/1.1`

Response:
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

{"errors":[{"detail":"Message sent on bus 0, but bus 1 is in the bus-off state"}]}

```

**Example**

Request `GET /?id=123&data=[] HTTP/1.1`

Response:
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

{"errors":[{"detail":"Application-specific error message"}]}
```
