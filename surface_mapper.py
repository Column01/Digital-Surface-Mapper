import serial.tools.list_ports
from printrun.printcore import printcore

from indicator import IndicatorReader


class SurfaceMapper:
    def __init__(self, printer_port, printer_baud, indicator_port, indicator_baud):
        self.printer_port = printer_port
        self.indicator_port = indicator_port

        self.printer_baud = printer_baud
        self.indicator_baud = indicator_baud

        self.printer = None
        self.indicator = None
    
    def connect_printer(self):
        if self.printer:
            self.printer.disconnect()
            self.printer = None
        self.printer = printcore(self.printer_port, self.printer_baud)

    def connect_indicator(self):
        if self.indicator:
            self.indicator = None
        self.indicator = IndicatorReader(self.indicator_port, self.indicator_baud)
        self.indicator.connect()


if __name__ == "__main__":
    com_ports = [f"- {comport.device}" for comport in serial.tools.list_ports.comports()]
    print("Choose your PRINTER port:")
    print("\n".join(com_ports))
    printer_port = input("Type full comport name: ")
    com_ports.remove(f"- {printer_port}")

    print("Choose your INDICATOR port:")
    print("\n".join(com_ports))
    indicator_port = input("Type full comport name: ")

    # Assuming that printer and indicator use this baud rate is relatively safe. If it's garbled for some people, support for setting baud can be added
    baud = 115200
    surface_mapper = SurfaceMapper(printer_port, baud, indicator_port, baud)
    surface_mapper.connect_indicator()
    print(surface_mapper.indicator.get_readings(10, 0.5))
