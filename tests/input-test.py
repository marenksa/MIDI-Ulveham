import rtmidi

def readMessage(msg, data):
    print(msg)

midiIn = rtmidi.MidiIn()

print(f"Found ports: {midiIn.get_ports()}")

midiIn.open_port(0)

midiIn.set_callback(readMessage)

with midiIn:
    while True:
        midiIn.get_message()

