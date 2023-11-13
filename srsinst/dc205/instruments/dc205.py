
import time
from srsgui import Instrument, SerialInterface, FindListInput, IntegerListInput
from .components import Config, Setting, Scan, Setup, Interface, Status


class DC205(Instrument):
    _IdString = 'DC205'

    available_interfaces = [
        [
            SerialInterface,
            {
                'port': FindListInput(),
                'baud_rate': IntegerListInput([9600, 19200, 38400, 57600, 115200], 4)
            }
        ]
    ]

    def __init__(self, interface_type=None, *args):
        super().__init__(interface_type, *args)
        self.set_term_char(b'\n')

        self.config = Config(self)
        self.setting = Setting(self)
        self.scan = Scan(self)
        self.setup = Setup(self)
        self.interface = Interface(self)
        self.status = Status(self)

    def connect(self, interface_type, *args):
        super().connect(interface_type, *args)
        self.send('TOKN OFF')

    def reset(self):
        self.interface.reset()

    def get_status(self):
        return self.status.get_status_text()

    
if __name__ == '__main__':
    from srsinst.dc205 import DC205
    vs = DC205('serial', 'COM9', 9600)
    vs.reset()
    print(vs.interface.id_string)
    vs.config.range = 'RANGE1'
    vs.close()
