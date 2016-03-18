#!/usr/bin/python3
#TODO: OSErrors are thrown if the CAN bus goes down, need to do threaded Exception handling
#      See http://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
#TODO: Check for BUS-OFF before attempting to send
import CAN
import CANopen
from functools import reduce
from operator import xor
import RPi.GPIO as GPIO
import signal
from threading import Event, Thread, Timer
from time import sleep, time
from sys import exit

DEFAULT_CAN_INTERFACE = "vcan0"
REDUNDANT_CAN_INTERFACE = "vcan1"

PIN_ENABLE_N = 42
PIN_ADDRESS_N = list(range(34, 41))
PIN_ADDRESS_PARITY_N = 41
PIN_RUNLED0 = 2
PIN_ERRLED0 = 3
PIN_RUNLED1 = 4
PIN_ERRLED1 = 5

class CANopenIndicator:
    OFF = {'DutyCycle': 0, 'Frequency': 2.5}
    FLASH1 = {'DutyCycle': 16.67, 'Frequency': 0.833}
    #FLASH2 = {} Cannot accomplish with PWM
    #FLASH3 = {} Cannot accomplish with PWM
    BLINK = {'DutyCycle': 50, 'Frequency': 2.5}
    FLICKER = {'DutyCycle': 50, 'Frequency': 10}
    ON = {'DutyCycle': 100, 'Frequency': 2.5}

    def __init__(self, channel, state):
        GPIO.setup(channel, GPIO.OUT)
        self._pwm = GPIO.PWM(channel, state.get('Frequency'))
        self._pwm.start(state.get('DutyCycle'))

    def set_state(self, state):
        self._pwm.ChangeDutyCycle(state.get('DutyCycle'))
        self._pwm.ChangeFrequency(state.get('Frequency'))

class IntervalTimer(Thread):
    def __init__(self, interval, function, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        super().__init__(args=args, kwargs=kwargs)
        self.stopped = Event()
        self.function = function
        self.interval = interval

    def run(self):
        while not self.stopped.wait(self.interval):
            self.function(*self._args, **self._kwargs)

    def cancel(self):
        self.stopped.set()

class ResetNode(Exception):
    pass

class ResetCommunication(Exception):
    pass

def sigterm_handler(signum, msg):
    global error_indicator_timer, runled0, errled0, runled1, errled1
    reset_timers()
    error_indicator_timer.cancel()
    runled0.set_state(CANopenIndicator.OFF)
    errled0.set_state(CANopenIndicator.ON)
    runled1.set_state(CANopenIndicator.OFF)
    errled1.set_state(CANopenIndicator.ON)
    GPIO.cleanup()
    exit()

def millitime():
    return int(round(time() * 1000))

def set_nmt_state(state):
    global nmt_state, runled0
    nmt_state = state
    if state == CANopen.NMT_STATE_PREOPERATIONAL:
        indicator_state = CANopenIndicator.BLINK
    elif state == CANopen.NMT_STATE_OPERATIONAL:
        indicator_state = CANopenIndicator.ON
    elif state == CANopen.NMT_STATE_STOPPED:
        indicator_state = CANopenIndicator.FLASH1
    else:
        indicator_state = CANopenIndicator.OFF
    runled0.set_state(indicator_state)

def get_error_indicator_state(bus):
    err_state = bus.get_state()
    if err_state == CAN.Bus.STATE_ERROR_ACTIVE:
        indicator_state = CANopenIndicator.OFF
    elif err_state == CAN.Bus.STATE_ERROR_PASSIVE:
        indicator_state = CANopenIndicator.FLASH1
    else: # BUS-OFF or UNKNOWN
        indicator_state = CANopenIndicator.ON
    return indicator_state

def process_error_indicators():
    global default_bus, redundant_bus, errled0, errled1
    errled0.set_state(get_error_indicator_state(default_bus))
    errled1.set_state(get_error_indicator_state(redundant_bus))

def process_sync():
    global canopen_od, sync_timer
    is_sync_producer = (canopen_od.get(CANopen.ODI_SYNC).get(CANopen.ODSI_VALUE) & 0x40000000) != 0;
    sync_time = canopen_od.get(CANopen.ODI_SYNC_TIME).get(CANopen.ODSI_VALUE) / 1000000
    if sync_timer is not None and (sync_time != sync_timer.interval or nmt_state == CANopen.NMT_STATE_STOPPED):
        sync_timer.cancel()
    if is_sync_producer and sync_time != 0 and nmt_state != CANopen.NMT_STATE_STOPPED and (sync_timer is None or not sync_timer.is_alive()):
        sync_timer = IntervalTimer(sync_time, send_sync)
        sync_timer.start()

def send_sync():
    global active_bus, canopen_od
    sync_id = canopen_od.get(CANopen.ODI_SYNC).get(CANopen.ODSI_VALUE) & 0x3FF
    msg = CAN.Message(sync_id)
    active_bus.send(msg)

def send_bootup():
    global active_bus, node_id
    msg = CAN.Message((CANopen.FUNCTION_CODE_NMT_ERROR_CONTROL << CANopen.FUNCTION_CODE_BITNUM) + node_id)
    active_bus.sendall(msg)

def process_heartbeat_producer():
    global canopen_od, heartbeat_producer_timer
    heartbeat_time = canopen_od.get(CANopen.ODI_HEARTBEAT_PRODUCER_TIME).get(CANopen.ODSI_VALUE) / 1000
    if heartbeat_producer_timer is not None and heartbeat_time != heartbeat_producer_timer.interval:
        heartbeat_producer_timer.cancel()
    if heartbeat_time != 0 and (heartbeat_producer_timer is None or not heartbeat_producer_timer.is_alive()):
        heartbeat_producer_timer = IntervalTimer(heartbeat_time, send_heartbeat)
        heartbeat_producer_timer.start()

def send_heartbeat():
    global active_bus, node_id, nmt_state
    msg = CAN.Message((CANopen.FUNCTION_CODE_NMT_ERROR_CONTROL << CANopen.FUNCTION_CODE_BITNUM) + node_id, [nmt_state])
    active_bus.send(msg)

def heartbeat_consumer_timeout(id):
    global active_bus, canopen_od, nmt_state, node_id
    if nmt_state != CANopen.NMT_STATE_STOPPED:
        msg = CAN.Message((CANopen.FUNCTION_CODE_EMCY << CANopen.FUNCTION_CODE_BITNUM) + node_id, (CANopen.EMCY_HEARTBEAT_BY_NODE + id).to_bytes(2, byteorder='big') + canopen_od.get(CANopen.ODI_ERROR).get(CANopen.ODSI_VALUE).to_bytes(1, byteorder='big') + b'\x00\x00\x00\x00\x00')
        active_bus.send(msg)

def reset_timers():
    global heartbeat_consumer_timers, heartbeat_producer_timer, sync_timer
    for i,t in heartbeat_consumer_timers.items():
        t.cancel()
    heartbeat_consumer_timers = {}
    if heartbeat_producer_timer is not None and heartbeat_producer_timer.is_alive():
        heartbeat_producer_timer.cancel()
    if sync_timer is not None and sync_timer.is_alive():
        sync_timer.cancel()


signal.signal(signal.SIGTERM, sigterm_handler)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_ENABLE_N, GPIO.IN)
GPIO.setup(PIN_ADDRESS_N, GPIO.IN)
GPIO.setup(PIN_ADDRESS_PARITY_N, GPIO.IN)

runled0 = CANopenIndicator(PIN_RUNLED0, CANopenIndicator.OFF)
errled0 = CANopenIndicator(PIN_ERRLED0, CANopenIndicator.ON)
runled1 = CANopenIndicator(PIN_RUNLED1, CANopenIndicator.OFF)
errled1 = CANopenIndicator(PIN_ERRLED1, CANopenIndicator.ON)

nmt_state = None
error_indicator_timer = None
heartbeat_consumer_timers = {}
heartbeat_producer_timer = None
sync_timer = None

default_bus = CAN.Bus(DEFAULT_CAN_INTERFACE)
redundant_bus = CAN.Bus(REDUNDANT_CAN_INTERFACE)
active_bus = default_bus

error_indicator_timer = IntervalTimer(1, process_error_indicators)
error_indicator_timer.start()

while True:
    try:
        set_nmt_state(CANopen.NMT_STATE_INITIALISATION)
        # set_nmt_state(CANopen.NMT_STATE_RESET_NODE)
        reset_timers()
        if GPIO.input(PIN_ENABLE_N) == GPIO.HIGH:
            raise ResetNode
        canopen_od = CANopen.ObjectDictionary()
        while True:
            try:
                # set_nmt_state(CANopen.NMT_STATE_RESET_COMMUNICATION)
                reset_timers()
                address_n = [
                    GPIO.input(PIN_ADDRESS_N[6]),
                    GPIO.input(PIN_ADDRESS_N[5]),
                    GPIO.input(PIN_ADDRESS_N[4]),
                    GPIO.input(PIN_ADDRESS_N[3]),
                    GPIO.input(PIN_ADDRESS_N[2]),
                    GPIO.input(PIN_ADDRESS_N[1]),
                    GPIO.input(PIN_ADDRESS_N[0])]
                address_parity_n = reduce(xor, address_n)
                if address_parity_n != GPIO.input(PIN_ADDRESS_PARITY_N):
                    raise ResetCommunication

                node_id = 0
                for bit in address_n:
                    node_id = (node_id << 1) | (not bit)

                canopen_od = CANopen.ObjectDictionary({ # TODO: Include data types so there is a way to determine the length of values for SDO responses (currently always 4 bytes)
                    CANopen.ODI_DEVICE_TYPE: 0x00000000,
                    CANopen.ODI_ERROR: 0x00,
                    CANopen.ODI_SYNC: 0x40000000 + (CANopen.FUNCTION_CODE_SYNC << CANopen.FUNCTION_CODE_BITNUM),
                    CANopen.ODI_SYNC_TIME: 0, # 32-bit, in us
                    CANopen.ODI_EMCY_ID: (CANopen.FUNCTION_CODE_EMCY << CANopen.FUNCTION_CODE_BITNUM),
                    CANopen.ODI_HEARTBEAT_CONSUMER_TIME: CANopen.Object({
                        CANopen.ODSI_VALUE: 1,
                        CANopen.ODSI_HEARTBEAT_CONSUMER_TIME: 2000, # all nodes, 16-bit, in ms
                    }),
                    CANopen.ODI_HEARTBEAT_PRODUCER_TIME: 1000, # 16-bit, in ms
                    CANopen.ODI_IDENTITY: CANopen.Object({
                        CANopen.ODSI_VALUE: 4,
                        CANopen.ODSI_IDENTITY_VENDOR: 0x00000000,
                        CANopen.ODSI_IDENTITY_PRODUCT: 0x00000001,
                        CANopen.ODSI_IDENTITY_REVISION: 0x00000000,
                        CANopen.ODSI_IDENTITY_SERIAL: 0x00000001,
                    }),
                    CANopen.ODI_SDO_SERVER: CANopen.Object({
                        CANopen.ODSI_VALUE: 2,
                        CANopen.ODSI_SDO_SERVER_DEFAULT_CSID: (CANopen.FUNCTION_CODE_SDO_RX << CANopen.FUNCTION_CODE_BITNUM) + node_id,
                        CANopen.ODSI_SDO_SERVER_DEFAULT_SCID: (CANopen.FUNCTION_CODE_SDO_TX << CANopen.FUNCTION_CODE_BITNUM) + node_id,
                    }),
                    CANopen.ODI_SDO_CLIENT: CANopen.Object({
                        CANopen.ODSI_VALUE: 0, # Update when heartbeats received
                    }),
                    CANopen.ODI_TPDO1_COMMUNICATION_PARAMETER: CANopen.Object({
                        CANopen.ODSI_VALUE: 2,
                        CANopen.ODSI_TPDO_COMM_PARAM_ID: (1 << CANopen.TPDO_COMM_PARAM_RTR_BITNUM) + node_id,
                        CANopen.ODSI_TPDO_COMM_PARAM_TYPE: 0xFD, # RTR-only, asynchronous
                    }),
                    CANopen.ODI_TPDO1_MAPPING_PARAMETER: CANopen.Object({
                        CANopen.ODSI_VALUE: 2,
                        0x01: (CANopen.ODI_SYNC << 16) + (CANopen.ODSI_VALUE << 8) + 32,
                        0x02: (CANopen.ODI_SYNC_TIME << 16) + (CANopen.ODSI_VALUE << 8) + 32,
                    }),
                })

                send_bootup()
                set_nmt_state(CANopen.NMT_STATE_PREOPERATIONAL)

                while True: # This block should really be intterupt driven by active_bus.recv()
                    process_heartbeat_producer()
                    process_sync()
                    try:
                        msg = active_bus.recv()
                    except CAN.BusDown:
                        sleep(1)
                        continue
                    ts = millitime()
                    id = msg.arbitration_id
                    data = msg.data
                    rtr = msg.is_remote_frame
                    fc = (id >> CANopen.FUNCTION_CODE_BITNUM) & 0xF
                    if rtr:
                        target_node = id & 0x7F
                        if target_node == node_id or target_node == CANopen.BROADCAST_NODE_ID:
                            if fc == CANopen.FUNCTION_CODE_TPDO1 and nmt_state == CANopen.NMT_STATE_OPERATIONAL and (canopen_od.get(CANopen.ODI_TPDO1_COMMUNICATION_PARAMETER).get(CANopen.ODSI_TPDO_COMM_PARAM_ID) >> CANopen.TPDO_COMM_PARAM_RTR_BITNUM) & 1 == 1:
                                data = bytes()
                                for i in range(canopen_od.get(CANopen.ODI_TPDO1_MAPPING_PARAMETER).get(CANopen.ODSI_VALUE)):
                                    mapping = canopen_od.get(CANopen.ODI_TPDO1_MAPPING_PARAMETER).get(i + 1)
                                    data = data + canopen_od.get(mapping >> 16).get((mapping >> 8) & 0xFF).to_bytes((mapping & 0xFF) // 8, byteorder='big')
                                msg = CAN.Message((CANopen.FUNCTION_CODE_TPDO1 << CANopen.FUNCTION_CODE_BITNUM) + node_id, data)
                                active_bus.send(msg)
                            elif fc == CANopen.FUNCTION_CODE_NMT_ERROR_CONTROL:
                                data = [nmt_state]
                                msg = CAN.Message((CANopen.FUNCTION_CODE_NMT_ERROR_CONTROL << CANopen.FUNCTION_CODE_BITNUM) + node_id, data)
                                active_bus.send(msg)
                    elif fc == CANopen.FUNCTION_CODE_NMT:
                        command = id & 0x7F
                        if command == CANopen.NMT_NODE_CONTROL:
                            target_node = data[1]
                            if target_node == node_id or target_node == CANopen.BROADCAST_NODE_ID:
                                cs = data[0]
                                if cs == CANopen.NMT_NODE_CONTROL_START:
                                   set_nmt_state(CANopen.NMT_STATE_OPERATIONAL)
                                elif cs == CANopen.NMT_NODE_CONTROL_STOP:
                                   set_nmt_state(CANopen.NMT_STATE_STOPPED)
                                elif cs == CANopen.NMT_NODE_CONTROL_PREOPERATIONAL:
                                   set_nmt_state(CANopen.NMT_STATE_PREOPERATIONAL)
                                elif cs == CANopen.NMT_NODE_CONTROL_RESET_NODE:
                                   raise ResetNode
                                elif cs == CANopen.NMT_NODE_CONTROL_RESET_COMMUNICATION:
                                    raise ResetCommunication
                    elif fc == CANopen.FUNCTION_CODE_SDO_RX and nmt_state != CANopen.NMT_STATE_STOPPED:
                        if id == canopen_od.get(CANopen.ODI_SDO_SERVER).get(CANopen.ODSI_SDO_SERVER_DEFAULT_CSID):
                            ccs = (data[0] >> CANopen.SDO_CCS_BITNUM) & (2 ** CANopen.SDO_CCS_LENGTH - 1)
                            if len(data) >= 4:
                                odi = (data[1] << 8) + data[2]
                                odsi = data[3]
                                if odi in canopen_od:
                                    obj = canopen_od.get(odi)
                                    if odsi in obj:
                                        if ccs == CANopen.SDO_CCS_UPLOAD:
                                            scs = CANopen.SDO_SCS_UPLOAD
                                            sdo_data = obj.get(odsi)
                                        elif ccs == CANopen.SDO_CCS_DOWNLOAD:
                                            scs = CANopen.SDO_SCS_DOWNLOAD
                                            n = (data[0] >> CANopen.SDO_N_BITNUM) & (2 ** CANopen.SDO_N_LENGTH - 1)
                                            canopen_od.update({odi: int.from_bytes(data[4:], byteorder='big')}) # Could be data[4:7-n], or different based on data type
                                            sdo_data = 0
                                        else:
                                            scs = CANopen.SDO_CS_ABORT
                                            sdo_data = CANopen.SDO_ABORT_INVALID_CS
                                    else:
                                        scs = CANopen.SDO_CS_ABORT
                                        sdo_data = CANopen.SDO_ABORT_SUBINDEX_DNE
                                else:
                                    scs = CANopen.SDO_CS_ABORT
                                    sdo_data = CANopen.SDO_ABORT_OBJECT_DNE
                            else:
                                odi = 0x0000
                                odsi = 0x00
                                scs = CANopen.SDO_CS_ABORT
                                sdo_data = CANopen.SDO_ABORT_GENERAL # Don't see one specifically for sending not enough data bytes in the CAN msg (malformed SDO msg)
                            id = canopen_od.get(CANopen.ODI_SDO_SERVER).get(CANopen.ODSI_SDO_SERVER_DEFAULT_SCID)
                            sdo_data = sdo_data.to_bytes(4, byteorder='big')
                            n = 4 - len(sdo_data)
                            data = [(scs << CANopen.SDO_SCS_BITNUM) + (n << CANopen.SDO_N_BITNUM) + (1 << CANopen.SDO_E_BITNUM) + (1 << CANopen.SDO_S_BITNUM), (odi >> 8), (odi & 0xFF), (odsi)] + list(sdo_data)
                            msg = CAN.Message(id, data)
                            active_bus.send(msg)
                    elif fc == CANopen.FUNCTION_CODE_NMT_ERROR_CONTROL:
                        producer_id = id & 0x7F
                        if producer_id in heartbeat_consumer_timers:
                            heartbeat_consumer_timers.get(producer_id).cancel()
                        heartbeat_consumer_timer = Timer(canopen_od.get(CANopen.ODI_HEARTBEAT_CONSUMER_TIME).get(CANopen.ODSI_HEARTBEAT_CONSUMER_TIME) / 1000, heartbeat_consumer_timeout, [producer_id])
                        heartbeat_consumer_timer.start()
                        heartbeat_consumer_timers.update({producer_id: heartbeat_consumer_timer})
            except ResetCommunication:
                pass
    except ResetNode:
        pass
