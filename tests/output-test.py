import rtmidi

midiOut = rtmidi.MidiOut() # Creates an instance of the MidiOut class

print(f"Found ports: {midiOut.get_ports()}") # Writes available ports to the terminal

midiOut.open_port(1) # Opens the second port on the list

with midiOut:
    midiOut.send_message([144, 60, 66]) # Sends a message to the device on port 1 (second port)

del midiOut # Cleans up midiIn instance
