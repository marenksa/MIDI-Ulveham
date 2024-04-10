import rtmidi
import time

midiOut = rtmidi.MidiOut()

print(f"Found ports: {midiOut.get_ports()}")

midiOut.open_port(1)

with midiOut:
    midiOut.send_message([144, 60, 67])
    time.sleep(1.0)
    midiOut.send_message([67, 67]) # running status!!

