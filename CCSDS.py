#!/usr/bin/python3

import errno
from fcntl import ioctl
import re
import socket
import struct
from subprocess import CalledProcessError, check_output

class SpacePacket:

    PRIMARY_HEADER_FORMAT = "=3H"
    PRIMARY_HEADER_SIZE = struct.calcsize(PRIMARY_HEADER_FORMAT)

    PRIMARY_HEADER_VERSION_BITNUM = 0
    PRIMARY_HEADER_TYPE_BITNUM = 3
    PRIMARY_HEADER_SECONDARY_HEADER_FLAG_BITNUM = 4
    PRIMARY_HEADER_APP_ID_BITNUM = 5
    PRIMARY_HEADER_SEQUENCE_FLAGS_BITNUM = 16
    PRIMARY_HEADER_SEQUENCE_COUNT_BITNUM = 18
    PRIMARY_HEADER_NAME = 18
    PRIMARY_HEADER_DATA_LENGTH_BITNUM = 32

    TYPE_TELEMETRY = 0
    TYPE_COMMAND = 1

    IDLE_PACKET_APP_ID = 2**11 - 1

    def __init__(self, type, app_id, data, *args, **kwargs):

        self.version = 0
        self.secondary_header_flag = 0
        self.sequence_flags = 0
        self.sequence_count = 0

        if type != self.TYPE_TELEMETRY and type != self.TYPE_COMMAND:
            raise ValueError("Type is not valid")
        self.type = 0

        if (not isinstance(app_id, int)) or app_id < 0 or app_id >= 2**11:
            raise ValueError("Application ID must be a positive integer less than " + str(2**11))
        self.app_id = app_id

        if len(data) >= 2**16:
            raise ValueError("Data must be less than " + str(2**16) + " bytes")

        if 'sequence_flags' in kwargs:
            if (not isinstance(kwargs['sequence_flags'], int)) or kwargs['sequence_flags'] < 0 or kwargs['sequence_flags'] > 4:
                raise ValueError("Sequence Flags must be a positive integer less than 4")
            self.sequence_flags = kwargs['sequence_flags']

        if 'sequence_count' in kwargs:
            if (not isinstance(kwargs['sequence_count'], int)) or kwargs['sequence_count'] < 0 or kwargs['sequence_count'] >= 2**14:
                raise ValueError("Sequence Count must be a positive integer less than " + str(2**14))
            self.sequence_count = kwargs['sequence_count']

        if 'secondary_header' in kwargs:
            if app_id == self.IDLE_PACKET_APP_ID:
                raise ValueError("Secondary Header is not allowed for Idle Packets")
            self.secondary_header_flag = 1
            self.data = bytearray(kwargs['secondary_header']) + bytearray(data)
        else:
            self.data = bytearray(data)

    def __bytes__(self):
        primary_header_1 = (
            (self.version << self.PRIMARY_HEADER_VERSION_BITNUM) +
            (self.type << self.PRIMARY_HEADER_TYPE_BITNUM) +
            (self.secondary_header_flag << self.PRIMARY_HEADER_SECONDARY_HEADER_FLAG_BITNUM) +
            (self.app_id << self.PRIMARY_HEADER_APP_ID_BITNUM))
        primary_header_2 = (
            (self.sequence_flags << (self.PRIMARY_HEADER_SEQUENCE_FLAGS_BITNUM - 16)) +
            (self.sequence_count << (self.PRIMARY_HEADER_SEQUENCE_COUNT_BITNUM - 16)))
        primary_header_3 = len(self.data) - 1
        return struct.pack(self.PRIMARY_HEADER_FORMAT + str(primary_header_3) + "s", primary_header_1, primary_header_2, primary_header_3, self.data)

    def from_bytes(b):
        data_length = len(b) - SpacePacket.PRIMARY_HEADER_SIZE
        primary_header_1, primary_header_2, primary_header_3, data = struct.unpack(SpacePacket.PRIMARY_HEADER_FORMAT + str(data_length) + "s", b)
        type = (primary_header_1 >> SpacePacket.PRIMARY_HEADER_TYPE_BITNUM) & 1
        app_id = (primary_header_1 >> SpacePacket.PRIMARY_HEADER_APP_ID_BITNUM) & 0x7FF
        data = data[:data_length]
        p = SpacePacket(type, app_id, data)
        p.version = primary_header_1 & 0x3
        p.secondary_header_flag = (primary_header_1 >> SpacePacket.PRIMARY_HEADER_SECONDARY_HEADER_FLAG_BITNUM) & 1
        p.sequence_flags = (prmary_header_2 >> (SpacePacket.PRIMARY_HEADER_SEQUENCE_FLAGS_BITNUM - 16)) & 0x2
        p.sequence_count = (prmary_header_2 >> (SpacePacket.PRIMARY_HEADER_SEQUENCE_COUNT_BITNUM - 16)) & 0x3FFF
        return p
