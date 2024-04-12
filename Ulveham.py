import rtmidi
import time
import re

# This class will handle the whole track
class Track:

    # Basic info
    bpm = 120
    beatsPerBar = 4
    score = []
    currentVoice = ''
    pedal = False

    time = {
        'whole': 1,
        'half': 1/2,
        'quart' : 1/4,
        'quart_dot' : 1/4 + 1/8,
        'eight' : 1/8,
        'sixteenth' : 1/16,
        'triplet_half': 1/3,
        'triplet_quart' : 1/6,
        'triplet_quart_dot': 1/6 + 1/12,
        'triplet_eight' : 1/12,
        'triplet_sixteenth': 1/16
    }
    sounds = { #Casio Privia PX-410R Appendix Documentation: [Bank Select Sound Code (4), Program Change Sound Code (3)]
        'MV' : [100, 0], # Main voice 
        'BV' : [52, 16] # Backing vocal
    }

    # How long should the note/rest be held
    def calc_note_length(self, time_key):
        
        # note length * beats per measure * 
        return self.time[time_key]*self.beatsPerBar*(60/self.bpm)

    # Send commands to MIDI device to change sound
    def change_sound(self, interface, sound):

        interface.send_message([0xB0, 0x00, self.sounds[sound][0]]) # Bank Select MSB
        interface.send_message([0xB0, 0x20, 0]) # Bank Select LSB
        interface.send_message([0xC0, self.sounds[sound][1]]) # Program Change

    # Reads in a score from a text file
    def add_score(self, scoreFile):
                
        with open(scoreFile, "r") as f:

            fromFile = []
            
            # Iterate through each line in the file
            for line in f:
                # Uses regex to find lines containing lists
                match = re.match(r'\[(.*?)\]', line)
                if match:
                    fromFile.append(eval(match.group(0))) # Convert it to a python list

            self.score = fromFile

    
    # Play the track indicated by the score
    def play(self, interface):

        interface.send_message([0xE0, 0, 64]) # Makes sure the pitch wheel is set correctly

        for item in self.score:
            key = item[0]

            # Play note from score
            if isinstance(key, int): 
                if not isinstance(item[3], bool): # Pitch is modified
                    interface.send_message([0xE0, 0, 64+item[3]]) # Modify pitch

                interface.send_message([0x90, key, item[2]]) # Note on
                time.sleep(self.calc_note_length(item[1])) # Hold
                interface.send_message([key, 0]) # Note "off"

                if not isinstance(item[3], bool): # If pitch is modified
                    interface.send_message([0xE0, 0, 64]) # Reset pitch wheel

            # "Play" rest
            elif key == '-':
                time.sleep(self.calc_note_length(item[1]))

            # Adjust pedal
            elif key == 'P':
                if self.pedal: # If pedal is on, turn it off
                    interface.send_message([0xB0, 0x40, 0]) 
                else: # If pedal is off, turn it on
                    interface.send_message([0xB0, 0x40, 127]) 
                self.pedal = not self.pedal # Set the pedal status to the opposite

            # Change sound
            elif key in self.sounds.keys(): 
                if self.currentVoice != item: # If it's the same sound, we don't have to "change" it
                    self.currentVoice = item
                    self.change_sound(interface, key) 

            # Ignore anything we don't recognise
            else:
                pass

    

# ------------------------------------------------------------------------------ #

def main():

    track = Track() # Make a track
    track.add_score("Vers1.txt") # Add the score

    # Interface for communication with the Casio
    midiOut = rtmidi.MidiOut()
    midiOut.open_port(1)

    with midiOut:  
        track.play(midiOut) # Play the track!
    del midiOut # Clean up

main()
