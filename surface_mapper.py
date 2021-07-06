import re
import threading

import serial.tools.list_ports
from printrun.eventhandler import PrinterEventHandler
from printrun.printcore import printcore

from indicator import IndicatorReader

ok_received = threading.Condition()


class RecvHandler(PrinterEventHandler):
    def __init__(self):
        PrinterEventHandler.__init__(self)
        self.clear()
    
    def clear(self):
        self.printer_response = []
    
    def on_recv(self, ln):
        self.printer_response.append(ln)
        if ln.startswith('ok'):
            with ok_received:
                ok_received.notify()


class SurfaceMapper:
    def __init__(self, printer_port, printer_baud, indicator_port, indicator_baud):
        self.printer_port = printer_port
        self.indicator_port = indicator_port

        self.printer_baud = printer_baud
        self.indicator_baud = indicator_baud

        self.printer = None
        self.indicator = None

        self.max_x = self.max_y = self.max_z = 0.0

        self.recv_handler = RecvHandler()
    
    def connect_printer(self):
        """Connects to the printer using Printcore
        """
        if self.printer:
            self.printer.disconnect()
            self.printer = None
        self.printer = printcore(self.printer_port, self.printer_baud)
        self.printer.addEventHandler(self.recv_handler)
        while not self.printer.online:
            continue

    def connect_indicator(self):
        """Connects to the indicator using the indicator reader class
        """
        if self.indicator:
            self.indicator = None
        self.indicator = IndicatorReader(self.indicator_port, self.indicator_baud)
        self.indicator.connect()

    def wait_for_ok(self):
        with ok_received:
            ok_received.wait()

    def send(self, gcode):
        self.recv_handler.clear()
        self.printer.send(gcode)
        self.wait_for_ok()
    
    def get_max_size(self):
        self.send("M211")
        for ln in self.recv_handler.printer_response:
            ln.replace("\n", "").strip()
            m = re.search(r'Max:\s+X([\d.-]+)\sY([\d.-]+)\sZ([\d.-]+)', ln)
            if m:
                self.max_x, self.max_y, self.max_z = [float(f) for f in m.groups()]


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
    surface_mapper.send("G28")
    print("Printer homed")
    print("Getting max printer size...")

    surface_mapper.get_max_size()
    if surface_mapper.max_x > 0.0:
        print(surface_mapper.max_x, surface_mapper.max_y, surface_mapper.max_z)

    print("Connecting to indicator...")
    surface_mapper.connect_indicator()
    print("Getting some readings for testing...")
    print(surface_mapper.indicator.get_readings(10, 0.5))
