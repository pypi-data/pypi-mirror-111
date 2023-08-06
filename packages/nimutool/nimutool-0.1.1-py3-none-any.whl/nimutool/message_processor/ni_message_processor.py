from nimutool.canbus import *
from .message_processor import *
import math
from struct import unpack


def is_high_range(number: int): 
    return number & (1 << 60) != 0

def unpack_20b_float(val, range_hi):
    shift = 13 if range_hi else 15
    return twos_comp(val, 20) / (1 << shift)

def parse_fixpoint(data):
    val = unpack('<Q', data)[0]
    vals = [unpack_20b_float((val >> shift) & 0xfffff, is_high_range(val)) for shift in [0, 20, 40]]
    error_flags = [val & (1 << i) != 0 for i in range(61, 64)]
    return vals, error_flags

def parse_imuloc(data):
    nid, x, y, z = unpack('<Bxhhh', data)
    return (nid, x, y, z)

def parse_temps(data):
    temp_hpca, temp_bmx, temp_cpu = unpack('hhhxx', data)
    return temp_hpca, temp_bmx, temp_cpu


class NimuMessageProcessorOld(MessageProcessorBase):

    MSG_HANDLERS = {
        0x000: {'name': 'sync', 'sensor': SensorModel.NotApplicable, 'type': None, 'frequency': 1, 'is_extended': False, 'parser': None},
        0x010: {'name': 'hpca gyro', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x020: {'name': 'bmx gyro', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x080: {'name': 'temp', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Temperature, 'frequency': 1, 'is_extended': False, 'parser': parse_temps},
        0x110: {'name': 'hpca acc', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x120: {'name': 'bmx acc', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x140: {'name': 'dcm', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Pose, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x150: {'name': 'pos', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Position, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x160: {'name': 'vel', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Velocity, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x170: {'name': 'imuloc', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.ImuPosition, 'frequency': 1, 'is_extended': False, 'parser': parse_imuloc},
        0x180: {'name': 'innovation', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Innovation, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x190: {'name': 'scl acc', 'sensor': SensorModel.SCLxxxx, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
    }

    def process_message(self, message: CanMessage, data_collection: CanMessageCollection) -> ProcessedCanDataItem:
        data_id, node_id = self.split_canid_to_msgid_and_nodeid(message.msg_id)
        hdlr = self.MSG_HANDLERS[data_id]
        parser = hdlr['parser']
        if parser:
            data = parser(message.data)
            return ProcessedCanDataItem(node_id, hdlr['sensor'], hdlr['type'], data)
        return None

    def canid2dataid(self, can_id):
        return can_id & 0xff0

    def split_canid_to_msgid_and_nodeid(self, can_id):
        return can_id & 0xff0, can_id & 0x00f


class NimuMessageProcessor(NimuMessageProcessorOld):

    MSG_HANDLERS = {
        0x000: {'name': 'sync', 'sensor': SensorModel.NotApplicable, 'type': None, 'frequency': 1, 'is_extended': False, 'parser': None},
        0x010: {'name': 'hpca acc', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x020: {'name': 'hpca gyro', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x090: {'name': 'bmx acc', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x0a0: {'name': 'bmx gyro', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x110: {'name': 'hpi acc', 'sensor': SensorModel.SCLxxxx, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x300: {'name': 'dcm', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Pose, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
        0x330: {'name': 'imuloc', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.ImuPosition, 'frequency': 1, 'is_extended': False, 'parser': parse_imuloc},
        0x340: {'name': 'innovation', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Innovation, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint},
    }
