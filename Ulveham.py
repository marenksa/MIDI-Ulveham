import rtmidi
import time

# This class will handle the whole track
class Track:

    # Basic info
    bpm = 130
    score = []
    currentVoice = ''

    rests = {
        '-': (2*60/bpm)/3, # 1/4th note triplet
        '_' : 60/bpm # 1/4th note
    }
    sounds = { #Casio Privia PX-410R Appendix Documentation: [Bank Select Sound Code (4), Program Change Sound Code (3)]
        'MV' : [100, 0], # Main voice 
        'BV' : [52, 16] # Backing vocal
    }

    # Send commands to MIDI device to change sound
    def change_sound(self, interface, sound):

        interface.send_message([176, 0, self.sounds[sound][0]]) # Bank Select MSB
        interface.send_message([176, 32, 0]) # Bank Select LSB
        interface.send_message([192, self.sounds[sound][1]]) # Program Change

    # Reads in a score from a text file
    def add_score(self, scoreFile):
                
        with open(scoreFile, "r") as f:

            bars = [x.strip().split(' ') for x in f.readlines()]
            
            for bar in bars:
                for i in range(len(bar)):
                    if bar[i].isdigit():
                        self.score.append(int(bar[i]))
                    else:
                        self.score.append(bar[i])

    
    # Play the track indicated by the score
    def play(self, interface):

        for item in self.score:
            # Play note from score
            if isinstance(item, int): 
                interface.send_message([144, item, 60]) # We could have just sent ...
                time.sleep(self.rests['-'])
                interface.send_message([item, 0]) # Release the key
            # "Play" rest
            elif item in self.rests.keys():
                time.sleep(self.rests[item])
            # Change sound
            elif item in self.sounds.keys(): 
                if self.currentVoice != item: # If it's the same sound, we don't have to "change" it
                    self.currentVoice = item
                    self.change_sound(interface, item) 
            # Ignore anything else
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
