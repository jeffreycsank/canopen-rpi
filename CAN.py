#!/usr/bin/python3

from array import array
import errno
import socket
import struct

class Frame:
    FORMAT = "=IB3x8s"
    SIZE = struct.calcsize(FORMAT)
    RTR_BITNUM = 30
    def __init__(self, id, data = [], rtr = 0):
        self.id = id
        self.data = data
        self.rtr = rtr
    def to_bytes(self):
        id = (self.rtr << self.RTR_BITNUM) + self.id
        dlc = len(self.data)
        data = array('B', self.data).tostring()
        data = data.ljust(8, b'\x00')
        return struct.pack(self.FORMAT, id, dlc, data)

class Bus:
    def __init__(self, device):
        self._s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self._s.bind((device,))
    def recv(self):
        try:
            frame = self._s.recv(Frame.SIZE)
        except OSError as e:
            if e.errno == errno.ENETDOWN:
                raise BusDown
            raise e
        id, dlc, data = struct.unpack(Frame.FORMAT, frame)
        rtr = (id >> Frame.RTR_BITNUM) & 1
        return Frame(id, data[:dlc], rtr)
    def send(self, frame: Frame):
        bytes_sent = self._s.send(frame.to_bytes())
        return bytes_sent
    def sendall(self, frame: Frame):
        bytes_sent = self._s.sendall(frame.to_bytes())
        return bytes_sent

class BusDown(Exception):
    pass
