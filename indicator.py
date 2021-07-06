import serial
import serial.tools.list_ports


class IndicatorReader:
    def __init__(self, com_port, baud):
        self.com_port = com_port
        self.baud = baud
        self.ser = None
    
    def connect(self):
        """ Opens the connection to the indicator """
        self.ser = serial.Serial(port=self.com_port, baudrate=self.baud)

    def is_ready(self):
        """ Checks if the serial connection is open """
        if self.ser is None:
            return False
        else:
            return self.ser.isOpen()
    
    def get_reading(self):
        """Returns a reading from the indicator

        Returns:
            tuple(value, unit): Returns a tuple containing the value and the measurement unit
        """
        if self.is_ready():
            self.ser.reset_input_buffer()
            line = self.ser.readline().strip(b"\r\n").decode().split(",")
            unit = "in" if line[1] == "1" else "mm"
            value = int(line[0]) / 2000 if unit == "in" else int(line[0]) / 100
            return value, unit
        else:
            return None


if __name__ == "__main__":
    com_ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print("Choose your com port:")
    print("\n".join(com_ports))
    com_port = input("Type full comport name: ")
    baud = 115200
    indicator_reader = IndicatorReader(com_port, baud)
    indicator_reader.connect()
    print(indicator_reader.get_reading())
