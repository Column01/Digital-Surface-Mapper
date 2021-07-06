# Digital-Surface-Mapper

Python and arduino program to map a surface with a cheap dial indicator
**I am not responsible for any damage to hardware when doing this. Proceed at your own risk**

### Table of Contents
- [Hardware](#hardware)
- [Wiring](#wiring)
- [Software](#software)

## Hardware

- Cheap chinese digital dial indicator with an "RS232" connection
- Arduino Nano or equivalent
- A computer to send the data too
- Soldering Iron

## Wiring

PLEASE, _PLEASE_, **PLEASE** ensure that all connections made are not shorting out. If they short out, you could damage your arduino or your indicator in the process!

### Micro USB dial indicator

This is for if your indicator has a Micro USB port on it that has the capability for the RS232 connection (Double check the seller page to ensure it has the connection, if not you may have to use the other section below

There are two methods, see each below and decide what you want to do.

You will need:

- USB A female breakout board **OR** the ability to cut and solder wires from a Micro USB cable.

#### Breakout board method

You will need wire the following breakout board pins to the arduino:

- `GND -> GND`
- `D+ -> Pin A0`
- `D- -> A1`
- `5v (sometimes labeled VCC or VBus on the board) -> 5v`

#### Cut and Solder method

Once cut, the cable should have at least 4 wires we need. You need to wire the cable to the following arduino pins:

- `Black (GND) -> GND`
- `Green (D+) -> A0`
- `White (D-) -> A1`
- `Red (5v) -> 5v`

I used some spare prototyping board and some pin headers to solder the cable to a convient ghetto breakout board that I could use dupont connectors to connect to the arduino

### Exposed port dial indicator

This is for if your indicator has an open port on the side for access to the data lines.

You will need:

- Thin gauge wire (18-24 AWG is probably good)
- Soldering iron and Solder
- Tools to dissassemble the indicator if needed (probably needed)

There should be 4 solder pads inside the indicator, you will need to solder wires to 3 out of the 4 pins.

Solder wires to: `DATA`, `CLOCK`, `GND`

Once wires are attached, you need to connect them to the arduino in the following way:

- `GND -> GND`
- `DATA -> A0`
- `CLOCK -> A1`

## Software

### Flashing the arduino code

Open the `.ino` file in the arduino IDE and select the correct COM port, and arduino version. Then just upload the sketch and it should be ready to go.

The arudino code is modified from a project by Paweł Stawicki. You can see it hosted on github here: https://github.com/stawel/dialIndicatorToSerial

### Using the python script

The python script is written for Python 3.8 or newer. Please ensure you install a version that is 3.8 or newer.

#### Dependencies

- `pyserial`
  - Install using `pip install pyserial` or `python -m pip install pyserial`

#### Running the program

- `python surface_mapper.py`
