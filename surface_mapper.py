import time
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

        self.ok_count = 0
    
    def connect_printer(self):
        """Connects to the printer using Printcore
        """
        if self.printer:
            self.printer.disconnect()
            self.printer = None
        self.printer = printcore(self.printer_port, self.printer_baud)
        self.printer.recvcb = self.recv_callback
        while not self.printer.online:
            continue

    def connect_indicator(self):
        """Connects to the indicator using the indicator reader class
        """
        if self.indicator:
            self.indicator = None
        self.indicator = IndicatorReader(self.indicator_port, self.indicator_baud)
        self.indicator.connect()
    
    def recv_callback(self, line):
        if 'ok' in line:
            self.ok_count += 1

    def wait_for_ok(self, num_oks):
        while self.ok_count < num_oks:
            time.sleep(0.1)

    def send_gcode_and_wait(self, gcode, num_oks=1):
        self.ok_count = 0
        self.printer.send(gcode)
        self.wait_for_ok(num_oks)


if __name__ == "__main__":
    # Get a list of com ports
    com_ports = [f"- {comport.device}" for comport in serial.tools.list_ports.comports()]

    # Ask the user for the printer port
    print("Choose your PRINTER port:")
    print("\n".join(com_ports))
    printer_port = input("Type full comport name: ")
    if f"- {printer_port}" not in com_ports:
        quit("Invalid device port!")
    com_ports.remove(f"- {printer_port}")

    # Ask the user for the indicator port
    print("Choose your INDICATOR port:")
    print("\n".join(com_ports))
    indicator_port = input("Type full comport name: ")
    if f"- {indicator_port}" not in com_ports:
        quit("Invalid device port!")

    # Assuming that printer and indicator use this baud rate is relatively safe. If it's garbled for some people, support for setting baud can be added
    baud = 115200

    # Make an instance of the surface mapper and get some readings from the indicator
    surface_mapper = SurfaceMapper(printer_port, baud, indicator_port, baud)

    print("Connecting to printer...")
    surface_mapper.connect_printer()
    print("Homing printer...")
    surface_mapper.send_gcode_and_wait("G28")
    print("Printer homed")

    print("Connecting to indicator...")
    surface_mapper.connect_indicator()
    print("Getting some readings for testing...")
    print(surface_mapper.indicator.get_readings(10, 0.5))
