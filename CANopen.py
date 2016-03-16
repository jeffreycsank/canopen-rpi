from collections import Mapping, MutableMapping

BROADCAST_NODE_ID = 0

# Function codes
FUNCTION_CODE_BITNUM = 7
FUNCTION_CODE_NMT = 0x0
FUNCTION_CODE_SYNC = 0x1
FUNCTION_CODE_EMCY = 0x1
FUNCTION_CODE_TIME_STAMP = 0x2
FUNCTION_CODE_TPDO1 = 0x3
FUNCTION_CODE_RPDO1 = 0x4
FUNCTION_CODE_TPDO2 = 0x5
FUNCTION_CODE_RPDO2 = 0x6
FUNCTION_CODE_TPDO3 = 0x7
FUNCTION_CODE_RPDO3 = 0x8
FUNCTION_CODE_TPDO4 = 0x9
FUNCTION_CODE_RPDO4 = 0xA
FUNCTION_CODE_SDO_TX = 0xB
FUNCTION_CODE_SDO_RX = 0xC
FUNCTION_CODE_NMT_ERROR_CONTROL = 0xE

# NMT commands
NMT_NODE_CONTROL = 0
NMT_NODE_CONTROL_START = 1
NMT_NODE_CONTROL_STOP = 2
NMT_NODE_CONTROL_PREOPERATIONAL = 128
NMT_NODE_CONTROL_RESET_NODE = 129
NMT_NODE_CONTROL_RESET_COMMUNICATION = 130
NMT_GFC = 1

# NMT states
NMT_STATE_INITIALISATION = 0
NMT_STATE_STOPPED = 4
NMT_STATE_OPERATIONAL = 5
NMT_STATE_PREOPERATIONAL = 127

# Emergency error codes
EMCY_RESET = 0x0000
EMCY_NONE = 0x0000
EMCY_GENERIC = 0x1000
EMCY_HEARTBEAT_BY_NODE = 0x8F00

# Object dictionary structure
OD_STRUCTURE_OBJECT_TYPE_BITNUM = 0
OD_STRUCTURE_DATA_TYPE_BITNUM = 8

# Object dictionary object type
OD_OBJECT_TYPE_NULL = 0
OD_OBJECT_TYPE_DOMAIN = 2
OD_OBJECT_TYPE_DEFTYPE = 5
OD_OBJECT_TYPE_DEFSTRUCT = 6
OD_OBJECT_TYPE_VAR = 7
OD_OBJECT_TYPE_ARRAY = 8
OD_OBJECT_TYPE_RECORD = 9

# Object dictionary indices and sub-indices
ODSI_VALUE = 0x00
ODSI_STRUCTURE = 0xFF
ODI_DATA_TYPE_BOOLEAN = 0x0001
ODI_DATA_TYPE_INTEGER8 = 0x0002
ODI_DATA_TYPE_INTEGER16 = 0x0003
ODI_DATA_TYPE_INTEGER32 = 0x0004
ODI_DATA_TYPE_UNSIGNED8 = 0x0005
ODI_DATA_TYPE_UNSIGNED16 = 0x0006
ODI_DATA_TYPE_UNSIGNED32 = 0x0007
ODI_DATA_TYPE_REAL32 = 0x0008
ODI_DATA_TYPE_VISIBLE_STRING = 0x0009
ODI_DATA_TYPE_OCTET_STRING = 0x000A
ODI_DATA_TYPE_UNICODE_STRING = 0x000B
ODI_DATA_TYPE_TIME_OF_DAY = 0x000C
ODI_DATA_TYPE_TIME_DIFFERENT = 0x000D
ODI_DATA_TYPE_DOMAIN = 0x000E
ODI_DATA_TYPE_INTEGER24 = 0x0010
ODI_DATA_TYPE_REAL64 = 0x0011
ODI_DATA_TYPE_INTEGER40 = 0x0012
ODI_DATA_TYPE_INTEGER48 = 0x0013
ODI_DATA_TYPE_INTEGER56 = 0x0014
ODI_DATA_TYPE_INTEGER64 = 0x0015
ODI_DATA_TYPE_UNSIGNED24 = 0x0016
ODI_DATA_TYPE_UNSIGNED40 = 0x0018
ODI_DATA_TYPE_UNSIGNED48 = 0x0019
ODI_DATA_TYPE_UNSIGNED56 = 0x001A
ODI_DATA_TYPE_UNSIGNED64 = 0x001B
ODI_DATA_TYPE_PDO_COMMUNICATION_PARAMETER = 0x0020
ODSI_DATA_TYPE_PDO_COMM_PARAM_ID = 0x01
ODSI_DATA_TYPE_PDO_COMM_PARAM_TYPE = 0x02
ODSI_DATA_TYPE_PDO_COMM_PARAM_INHIBIT_TIME = 0x03
ODSI_DATA_TYPE_PDO_COMM_PARAM_EVENT_TIMER = 0x05
ODSI_DATA_TYPE_PDO_COMM_PARAM_SYNC_START = 0x06
ODI_DATA_TYPE_PDO_MAPPING_PARAMETER = 0x002100
ODI_DATA_TYPE_SDO_PARAMETER = 0x002200
ODSI_DATA_TYPE_SDO_PARAM_CSID = 0x01
ODSI_DATA_TYPE_SDO_PARAM_SCID = 0x02
ODSI_DATA_TYPE_SDO_PARAM_NODE_ID = 0x03
ODI_DATA_TYPE_IDENTITY = 0x0023
ODSI_DATA_TYPE_IDENTITY_VENDOR = 0x01
ODSI_DATA_TYPE_IDENTITY_PRODUCT = 0x02
ODSI_DATA_TYPE_IDENTITY_REVISION = 0x03
ODSI_DATA_TYPE_IDENTITY_SERIAL = 0x04
ODI_DEVICE_TYPE = 0x1000
ODI_ERROR = 0x1001
ODI_SYNC = 0x1005
ODI_SYNC_TIME = 0x1006
ODI_EMCY_ID = 0x1014
ODI_HEARTBEAT_CONSUMER_TIME = 0x1016
ODSI_HEARTBEAT_CONSUMER_TIME = 0x01
ODI_HEARTBEAT_PRODUCER_TIME = 0x1017
ODI_IDENTITY = 0x1018
ODSI_IDENTITY_VENDOR = 0x01
ODSI_IDENTITY_PRODUCT = 0x02
ODSI_IDENTITY_REVISION = 0x03
ODSI_IDENTITY_SERIAL = 0x04
ODI_SDO_SERVER = 0x1200
ODSI_SDO_SERVER_DEFAULT_CSID = 0x01
ODSI_SDO_SERVER_DEFAULT_SCID = 0x02
ODI_SDO_CLIENT = 0x1280
ODSI_SDO_CLIENT_TX = 0x01
ODSI_SDO_CLIENT_RX = 0x02
ODSI_SDO_CLIENT_NODE_ID = 0x03
ODI_TPDO1_COMMUNICATION_PARAMETER = 0x1800
ODSI_TPDO_COMM_PARAM_ID = 0x01
ODSI_TPDO_COMM_PARAM_TYPE = 0x02
ODI_TPDO1_MAPPING_PARAMETER = 0x1A00

# SDO
SDO_N_BITNUM = 1
SDO_N_LENGTH = 2
SDO_E_BITNUM = 1
SDO_S_BITNUM = 0
SDO_CCS_BITNUM = 5
SDO_CCS_LENGTH = 3
SDO_CCS_DOWNLOAD = 1
SDO_CCS_UPLOAD = 2
SDO_SCS_BITNUM = 5
SDO_SCS_LENGTH = 3
SDO_SCS_DOWNLOAD = 3
SDO_SCS_UPLOAD = 2
SDO_CS_ABORT = 4
SDO_ABORT_INVALID_CS = 0x05040001
SDO_ABORT_OBJECT_DNE = 0x06020000
SDO_ABORT_SUBINDEX_DNE = 0x06090011
SDO_ABORT_GENERAL = 0x08000000

# PDO
TPDO_COMM_PARAM_RTR_BITNUM = 30

class ObjectDictionary(MutableMapping):
    def __init__(self, other=None, **kwargs):
        self.store = { # Defaults
            ODI_DATA_TYPE_BOOLEAN: Object({
                ODSI_VALUE: 0x00000001,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER8: Object({
                ODSI_VALUE: 0x00000008,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER16: Object({
                ODSI_VALUE: 0x00000010,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER32: Object({
                ODSI_VALUE: 0x00000020,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED8: Object({
                ODSI_VALUE: 0x00000008,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED16: Object({
                ODSI_VALUE: 0x00000010,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED32: Object({
                ODSI_VALUE: 0x00000020,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_REAL32: Object({
                ODSI_VALUE: 0x00000020,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_VISIBLE_STRING: Object({
                ODSI_VALUE: 0x00000000, # Implementation-specific
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_OCTET_STRING: Object({
                ODSI_VALUE: 0x00000000, # Implementation-specific
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNICODE_STRING: Object({
                ODSI_VALUE: 0x00000000, # Implementation-specific
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_TIME_OF_DAY: Object({
                ODSI_VALUE: 0x00000030,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_DOMAIN: Object({
                ODSI_VALUE: 0x00000000,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER24: Object({
                ODSI_VALUE: 0x00000018,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_REAL64: Object({
                ODSI_VALUE: 0x00000040,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER40: Object({
                ODSI_VALUE: 0x00000028,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER48: Object({
                ODSI_VALUE: 0x00000030,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER56: Object({
                ODSI_VALUE: 0x00000038,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_INTEGER64: Object({
                ODSI_VALUE: 0x00000040,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED24: Object({
                ODSI_VALUE: 0x00000018,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED40: Object({
                ODSI_VALUE: 0x00000028,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED48: Object({
                ODSI_VALUE: 0x00000030,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED56: Object({
                ODSI_VALUE: 0x00000038,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_UNSIGNED64: Object({
                ODSI_VALUE: 0x00000040,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED32 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFTYPE << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_PDO_COMMUNICATION_PARAMETER: Object({
                ODSI_VALUE: 0x06, # Implementation-specific
                ODSI_DATA_TYPE_PDO_COMM_PARAM_ID: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_PDO_COMM_PARAM_TYPE: ODI_DATA_TYPE_UNSIGNED8,
                ODSI_DATA_TYPE_PDO_COMM_PARAM_INHIBIT_TIME: ODI_DATA_TYPE_UNSIGNED16,
                ODSI_DATA_TYPE_PDO_COMM_PARAM_EVENT_TIMER: ODI_DATA_TYPE_UNSIGNED16,
                ODSI_DATA_TYPE_PDO_COMM_PARAM_SYNC_START: ODI_DATA_TYPE_UNSIGNED8,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED16 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFSTRUCT << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_PDO_MAPPING_PARAMETER: Object({
                ODSI_VALUE: 0x00, # Implementation-specific
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED16 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFSTRUCT << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_SDO_PARAMETER: Object({
                ODSI_VALUE: 0x03, # Implementation-specific
                ODSI_DATA_TYPE_SDO_PARAM_CSID: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_SDO_PARAM_SCID: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_SDO_PARAM_SCID: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_SDO_PARAM_NODE_ID: ODI_DATA_TYPE_UNSIGNED8,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED16 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFSTRUCT << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
            ODI_DATA_TYPE_IDENTITY: Object({
                ODSI_VALUE: 0x04, # Implementation-specific
                ODSI_DATA_TYPE_IDENTITY_VENDOR: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_IDENTITY_PRODUCT: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_IDENTITY_REVISION: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_DATA_TYPE_IDENTITY_SERIAL: ODI_DATA_TYPE_UNSIGNED32,
                ODSI_STRUCTURE: (ODI_DATA_TYPE_UNSIGNED16 << OD_STRUCTURE_DATA_TYPE_BITNUM) + (OD_OBJECT_TYPE_DEFSTRUCT << OD_STRUCTURE_OBJECT_TYPE_BITNUM)
            }),
        }
        self.update(other, **kwargs)

    def __getitem__(self, index):
        # TODO: Prevent reading of write-only indices
        obj = self.store[index]
#        if len(obj) == 0:
#            return obj.get(ODSI_VALUE)
        return obj

    def __setitem__(self, index, obj):
        if type(index) is not int:
            raise TypeError("CANopen object dictionary index must be an integer")
        if index < 0 or index >= 2 ** 16:
            raise IndexError("CANopen object dictionary index must be a positive 16-bit integer")
        if not isinstance(obj, Object):
            if type(obj) not in [bool, int, float, str]:
                raise TypeError("CANopen object dictionary can only consist of CANopen objects or one of bool, int, float, or str")
            obj = Object({ODSI_VALUE: obj})
        # TODO: Prevent writing of read-only indices
        self.store[index] = obj

    def __delitem__(self, index):
        del self.store[index]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def update(self, other=None, **kwargs):
        if other is not None:
            for index, obj in other.items() if isinstance(other, Mapping) else other:
                self[index] = obj
            for index, obj in kwargs.items():
                self[index] = obj

class Object(MutableMapping):
    def __init__(self, other=None, **kwargs):
        self.store = dict()
        self.update(dict(other, **kwargs))
        if ODSI_VALUE not in self:
            raise RuntimeError("CANopen object sub-index " + ODSI_VALUE + " is required")

    def __getitem__(self, subindex):
        # TODO: Prevent reading of write-only indices
        return self.store[subindex]

    def __setitem__(self, subindex, value):
        if type(subindex) is not int:
            raise TypeError("CANopen object sub-index must be an integer")
        if subindex < 0 or subindex >= 2 ** 8:
            raise IndexError("CANopen object sub-index must be a positive 8-bit integer")
        if type(value) not in [bool, int, float, str]:
            raise TypeError("CANopen objects can only be set to one of bool, int, float, or str")
        # TODO: Prevent writing of read-only indices
        self.store[subindex] = value

    def __delitem__(self, subindex):
        del self.store[subindex]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        if ODSI_STRUCTURE in self.store:
            structure = self.store[ODSI_STRUCTURE]
            data_type = (structure >> 8) & 0xFF
            object_type = structure & 0xFF
            if object_type in [OD_OBJECT_TYPE_ARRAY, OD_OBJECT_TYPE_RECORD]:
                return len(self.store) - 2 # Don't count sub-indices 0x00 and 0xFF
        return len(self.store) - 1 # Don't count sub-index 0

    def __getattr__(self, name):
        if name == "data_type":
            if ODSI_STRUCTURE in self.store:
                structure = self.store[ODSI_STRUCTURE]
                data_type = (structure >> 8) & 0xFF
                return data_type
        if name == "object_type":
            if ODSI_STRUCTURE in self.store:
                structure = self.store[ODSI_STRUCTURE]
                object_type = structure & 0xFF
                return object_type
        raise AttributeError("CANopen object does not contain attribute [" + name + "]")

    def update(self, other=None, **kwargs):
        if other is not None:
            for subindex, value in other.items() if isinstance(other, Mapping) else other:
                self[subindex] = value
            for subindex, value in kwargs.items():
                self[subindex] = value
