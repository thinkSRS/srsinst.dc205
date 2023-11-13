
from srsgui import Task
from srsgui import InstrumentInput, CommandInput, ListInput, FloatInput
from srsinst.dc205 import DC205, get_dc205, Keys
from srsinst.dc205.instruments.components import Config

InstName = 'Inst to config'
VoltageRange = 'Range'
OutputVoltage = 'Output voltage'
AutoRange = 'Auto range'


class SetOutput(Task):
    """
Set dc current output. With auto gain adjust on, press the 'Apply' button and
press the 'Run' button (green arrow in the toolbar) to complete the operation.
    """
    input_parameters = {
        InstName: InstrumentInput(),
        VoltageRange: ListInput([f'{key} V' for key in Config.RangeDict]),
        OutputVoltage: FloatInput(0.0, 'V', -101.0, 101.0, 1e-6),
        AutoRange: ListInput(['Off', 'On'], 1)
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.cs = get_dc205(self, self.get_input_parameter(InstName))

    def test(self):
        inputs = self.get_all_input_parameters()
        self.logger.info('Output setting')
        self.logger.info(inputs)

        output_state = self.cs.config.output
        self.cs.config.output = Keys.OFF

        if inputs[AutoRange] == 'On':
            self.cs.setting.set_voltage(inputs[OutputVoltage], True)
        else:
            self.cs.setting.set_voltage(inputs[OutputVoltage], False)

        if output_state == Keys.ON:
            self.cs.config.output = Keys.ON

    def cleanup(self):
        pass


class EnableOutput(Task):
    input_parameters= {
        InstName: InstrumentInput()
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.cs = get_dc205(self, self.get_input_parameter(InstName))

    def test(self):
        self.logger.info('Enable Output')
        self.cs.config.output = Keys.ON

    def cleanup(self):
        pass


class DisableOutput(Task):
    input_parameters = {
        InstName: InstrumentInput()
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.cs = get_dc205(self, self.get_input_parameter(InstName))

    def test(self):
        self.logger.info('Enable Output')
        self.cs.config.output = Keys.OFF

    def cleanup(self):
        pass
