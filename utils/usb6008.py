import nidaqmx
from nidaqmx.constants import TerminalConfiguration


class USB6008:
    def __init__(self):
        self.read_task = nidaqmx.Task()
        self.write_task = nidaqmx.Task()
        self.read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE)
        self.write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=0, max_val=5)
        self.read_task.start()
        self.write_task.start()

    def read(self):
        return self.read_task.read()

    def write(self, value):
        self.write_task.write(value)

    def close(self):
        self.write(0)
        self.read_task.close()
        self.write_task.close()


if __name__ == "__main__":
    import time

    usb6008 = USB6008()

    usb6008.write(2.5)
    time.sleep(1)
    print(usb6008.read())

    usb6008.close()
