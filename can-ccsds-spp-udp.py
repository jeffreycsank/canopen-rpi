#!/usr/bin/python3
import CAN
import CANopen
import CCSDS
from datetime import datetime
import errno
from math import modf
from select import select
import signal
import socket
from struct import pack
import sys
from time import time, mktime, sleep

CAN_LISTEN_INTERFACES = ["vcan0", "vcan1"] # Must be a list
CAN_SEND_INTERFACE = "vcan0"
UDP_LOCAL_IP = "localhost"
UDP_LOCAL_READ_PORT = 5084
UDP_LOCAL_WRITE_PORT = 5082
UDP_REMOTE_IP = "10.10.5.29" # Must be on same network as UDP_LISTEN_IP or OSError is thrown
UDP_REMOTE_WRITE_PORT = 5083
UDP_MAX_PACKET_SIZE = 1024 # Absolute maximum of 65535

CCSDS_APP_ID = 0x3E

def sigterm_handler(signum, frame):
    sys.exit()

signal.signal(signal.SIGTERM, sigterm_handler)

sockets = []
for interface in CAN_LISTEN_INTERFACES:
    can_socket = CAN.Bus(interface)
    sockets.append(can_socket)
for s in sockets:
    if s.getsockname()[0] == CAN_SEND_INTERFACE:
      can_socket = s
      break

udp_write_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#udp_write_socket.bind((UDP_LOCAL_IP, UDP_LOCAL_WRITE_PORT))

udp_read_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_read_socket.bind((UDP_LOCAL_IP, UDP_LOCAL_READ_PORT))
sockets.append(udp_read_socket)
#buffer = bytearray(15 * 8)
buffer = bytearray(1)

while True:
    try:
        rlist, _, _ = select(sockets, [], [])
        for s in rlist:
            socket_type = s.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE)
            if isinstance(s, CAN.Bus):
                msg = s.recv()
                fc = (msg.arbitration_id >> CANopen.FUNCTION_CODE_BITNUM) & 0xF
                if fc == CANopen.FUNCTION_CODE_TPDO1:
                    node_id = msg.arbitration_id & 0x3F
                    #buffer[((node_id - 1) * 8):(((node_id - 1) * 8) + 7)] = bytes(msg.data).ljust(8, b'\x00')
                    buffer[0] = buffer[0] + 1
                elif fc == CANopen.FUNCTION_CODE_SYNC:
                    (subseconds, seconds) = modf(time() - mktime((1980, 1, 1, 0, 0, 0, 1, 1, 0))) # Could use (int(diff/1),diff%1) instead of modf
                    seconds += 5 * 3600 # Offset for Central Time
                    ts = pack(">IH", int(seconds), int(subseconds * (2 ** 16)))
                    packet = CCSDS.SpacePacket(CCSDS.SpacePacket.TYPE_TELEMETRY, CCSDS_APP_ID, bytes(buffer), sequence_flags=0x3, secondary_header=ts)
                    packet = bytearray(bytes(packet))
                    udp_write_socket.sendto(bytes(packet), (UDP_REMOTE_IP, UDP_REMOTE_WRITE_PORT))
                    print("Sent CCSDS Space Packet with " + str(int(buffer[0])) + " operational modules")
                    #buffer = bytearray(15 * 8)
                    buffer = bytearray(1)
            elif socket_type == socket.SOCK_DGRAM:
                data = s.recv(UDP_MAX_PACKET_SIZE)
                packet = CCSDS.SpacePacket.from_bytes(data)
                if packet.type == CCSDS.SpacePacket.TYPE_COMMAND and packet.app_id == CCSDS_APP_ID:
                    can_socket.send(packet.data) # Need to parse and strip off secondary header
    except CAN.BusDown:
        sleep(1)
