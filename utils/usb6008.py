import nidaqmx
from nidaqmx.constants import TerminalConfiguration


class USB6008:
    def __init__(self):
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.DIFF)
        self.task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=0, max_val=5)
        self.task.timing.cfg_samp_clk_timing(1000, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        self.task.start()

    def read(self):
        return self.task.read()

    def write(self, value):
        self.task.write(value)

    def close(self):
        self.write(0)
        self.task.stop()
        self.task.close()
