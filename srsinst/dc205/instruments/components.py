
import time

from srsgui import Component
from srsgui import GetCommand, \
                   IntCommand, IntGetCommand, \
                   BoolCommand, BoolGetCommand, \
                   FloatCommand, DictCommand

from srsgui import IntIndexCommand, IntIndexGetCommand, \
                   BoolIndexCommand, BoolIndexGetCommand, \
                   DictGetCommand

from .keys import Keys


def round_float(number, digits=4):
    """
    Round a float to the number of digits
    """
    f = '{{:.{}e}}'.format(digits)
    return float(f.format(number))


class Config(Component):

    RangeDict = {
        Keys.RANGE1: 0,
        Keys.RANGE10: 1,
        Keys.RANGE100: 2,
    }

    IsolationDict = {
        Keys.GROUND: 0,
        Keys.FLOAT: 1
    }

    SensingDict = {
        Keys.TWOWIRE: 0,
        Keys.FOURWIRE: 1
    }
    
    OffOnDict = {
        Keys.OFF: 0,
        Keys.ON: 1
    }

    voltage_range = DictCommand('RNGE', RangeDict)
    isolation = DictCommand('ISOL', IsolationDict)
    remote_sensing = DictCommand('SENS', SensingDict)
    output = DictCommand('SOUT', OffOnDict)

    def set_range(self, voltage):
        """
        Set to the minimum range that can accommodate the voltage
        """
        abs_volt = abs(voltage)
        if abs_volt > 101.0:
            raise ValueError('Cannot set to voltage exceeding 101 V')

        temp_range = Keys.RANGE1
        if abs_volt > 10.0:
            temp_range = Keys.RANGE100
        elif abs_volt > 1.0:
            temp_range = Keys.RANGE10
            
        current_range = self.voltage_range
        if temp_gain != current_gain:
            output_state = self.output
            self.output = Keys.OFF
            self.voltage_range = temp_range
            self.output = output_state
            if output_state == Keys.ON:
                time.sleep(0.25)

    def enable_output(self, state=True):
        if state:
            self.output = Keys.ON
        else:
            self.output = Keys.OFF

    def disable_output(self, state=True):
        if state:
            self.output = Keys.OFF
        else:
            self.output = Keys.ON

    allow_run_button = [enable_output, disable_output]


class Setting(Component):
    voltage = FloatCommand('VOLT', unit='V', min=-101.0, max=101.0, step=1e-3)

    def set_voltage(self, voltage, auto_range=False):
        if auto_range:
            self._parent.config.set_range(voltage)
        self.voltage = round_float(voltage)

class Scan(Component):
    ShapeDict = {
        Keys.ONEDIR: 0,
        Keys.UPDN: 1
    }
    CycleDict = {
        Keys.ONCE: 0,
        Keys.REPEAT: 1
    }
    
    ArmedDict = {
        Keys.IDLE: 0,
        Keys.ARMED: 1
    }
    
    ArmedStatusDict = {
        Keys.IDLE: 0,
        Keys.ARMED: 1,
        Keys.SCANNING: 2
    }
    
    scan_range = DictCommand('SCAR', Config.RangeDict)
    beginning_voltage = FloatCommand('SCAB', unit='V', min=-101.0, max=101.0, step=1e-3)
    ending_voltage = FloatCommand('SCAE', unit='V', min=-101.0, max=101.0, step=1e-3)
    time = FloatCommand('SCAT', unit='s', min=0.1, max=9999.9, step=0.1)
    shape = DictCommand('SCAS', ShapeDict)
    cycle = DictCommand('SCAC', CycleDict)
    display = DictCommand('SCAD', Config.OffOnDict)
    arm_state = DictCommand('SCAA', ArmedDict, ArmedStatusDict)
    
    def arm(self):
        self.comm.send('SCAA 1')

    def trigger(self):        
        self.comm.send('*TRG')

    def start(self):
        self.arm()
        self.trigger()

    def cancel(self):
        self.comm.send('SCAA 0')

    allow_run_button = [start, cancel]

    
    
class Setup(Component):
    key_click = DictCommand('KCLK', Config.OffOnDict)
    alarm = DictCommand('ALRM', Config.OffOnDict)


class Interface(Component):
    id_string = GetCommand('*IDN')
    token_mode = DictCommand('TOKN', Config.OffOnDict)
    operation_complete = BoolGetCommand('*OPC')
    overload = BoolGetCommand('OVLD')

    exclude_capture = [token_mode]

    def cancel_operation_complete(self):
        self.comm.send('*OPC')
        
    def reset(self):
        self.comm.send('*RST')
        time.sleep(2.0)
        self.token_mode = Keys.OFF

    allow_run_button = [cancel_operation_complete, reset]


class Status(Component):
    InterlockDict = {
        Keys.OPEN: 0,
        Keys.CLOSED: 1
    }
    
    StatusBitDict = {
        Keys.DCSB: 0,
        Keys.ESB: 5,
        Keys.MSS: 6,
    }
    EventStatusBitDict = {
        Keys.OPC: 0,
        Keys.QYE: 2,
        Keys.DDE: 3,
        Keys.EXE: 4,
        Keys.CME: 5,
        Keys.URQ: 6
    }

    SourceConditionBitDict = {
        Keys.OVERLOAD_BIT: 0,
        Keys.INTERLOCK_BIT: 1,
    }

    SourceEventBitDict = {
        Keys.SCAN_COMPLETED_BIT: 6,
        Keys.SCAN_CANCELLED_BIT: 7
    }
    
    ExecuteErrorDict = {
        'No Error': 0,
        'Illegal value': 1,
        'Wrong token': 2,
        'Invalid bit': 3,
        'Queue full': 4,
        'Not compatible': 5
    }
    CommandErrorDict = {
        'No error': 0,
        'Illegal command': 1,
        'Undefined command': 2,
        'Illegal query': 3,
        'Illegal set': 4,
        'Missing parameter': 5,
        'Extra parameter': 6,
        'Null parameter': 7,
        'Buffer Overflow': 8,
        'Bad floating-point': 9,
        'Bad integer': 10,
        'Bad integer token': 11,
        'Bad token value': 12,
        'Bad hex block': 13,
        'Unknown token': 14
    }
    interlock = DictCommand('ILOC', InterlockDict)
    overload = BoolCommand('OVLD')
    
    status_byte = IntGetCommand('*STB')
    event_status_byte = IntGetCommand('*ESR')
    event_status_enable_byte = IntCommand('*ESE')
    last_execution_error = DictGetCommand('LEXE', ExecuteErrorDict)
    last_command_error = DictGetCommand('LCME', CommandErrorDict)
    
    source_condition_byte = IntCommand('DCCR')
    source_positive_transition_byte = IntCommand('DCPT')
    source_negative_transition_byte = IntCommand('DCNT')
    
    source_event_byte = IntCommand('DCEV')
    source_event_enable_byte = IntCommand('DCEN')    
    
    def __init__(self, parent):
        super().__init__(parent)
        # IndexCommand needs to be initialized to work correctly with multiple instances
        self.service_request_enable_bits = BoolIndexCommand('*SRE', 7, 0, Status.StatusBitDict)
        self.event_status_bits = BoolIndexGetCommand('*ESR', 7, 0, Status.EventStatusBitDict)
        self.event_status_enable_bits = BoolIndexCommand('*ESE', 7, 0, Status.EventStatusBitDict)
        
        self.source_condition_bits = BoolIndexGetCommand('DCCR',7, 0, Status.SourceConditionBitDict )
        self.source_positive_transition_bits = BoolIndexGetCommand('DCPT',7, 0, Status.SourceConditionBitDict )
        self.source_negative_transition_bits = BoolIndexGetCommand('DCNT',7, 0, Status.SourceConditionBitDict )
        
        self.source_event_bits = BoolIndexGetCommand('DCEV', 7, 0, Status.SourceEventBitDict)
        self.source_event_enable_bits = BoolIndexCommand('DCEN', 7, 0, Status.SourceEventBitDict)
        
        self.add_parent_to_index_commands()

    def clear(self):
        """ Clear the event status register (ESR)
        """
        self.comm.send('*CLS')

    allow_run_button = [clear]

    def get_status_text(self):
        msg = ''
        status_byte = self.status_byte
        if self.StatusBitDict[Keys.ESB]:
            event = self.event_status_byte & 0x3C  # discard OPC and undef bits
            for key, val in self.EventStatusBitDict.items():
                if 2 ** val & event:
                    msg += 'Event bit {}, {} is set, '.format(val, key)

        if msg == '':
            msg = 'OK,'
        return msg[:-1]
