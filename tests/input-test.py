import rtmidi

def read_message(message, data):
    print(message) # Writes message to the terminal

midiIn = rtmidi.MidiIn() # Creates an instance of the MidiIn class

print(f"Found ports: {midiIn.get_ports()}") # Writes available ports to the terminal

midiIn.open_port(0) # Opens the first available port

midiIn.set_callback(read_message) # Sets callback-function for handling MIDI messages

with midiIn:
    input("Press enter to quit\n") # Waits for user input to terminate

del midiIn # Cleans up midiIn instance
