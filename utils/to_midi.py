import csv
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo, second2tick

NOTES_FLAT = ['C', 'D-', 'D', 'E-', 'E', 'F', 'G-', 'G', 'A-', 'A', 'B-', 'B']
NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def NoteToMidi(KeyOctave):
    # KeyOctave is formatted like 'C#3'
    key = KeyOctave[:-1]  # eg C, Db
    octave = KeyOctave[-1]   # eg 3, 4
    answer = -1

    try:
        if '-' in key:
            pos = NOTES_FLAT.index(key)
        else:
            pos = NOTES_SHARP.index(key)
    except:
        print(KeyOctave == 'rest' )
        print('The key is not valid', key)
        return None

    answer += pos + 12 * (int(octave) + 1) + 1
    return answer

def toMIDI(data, name):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))

    for datum in data:
        if datum:
            note = str(datum[0])
            duration = float(datum[1])/4
            if note and not note == 'rest': #eval(note)[0]
                if '[' in note:
                    for n in eval(note):
                        note_number = NoteToMidi(n)
                        track.append(Message('note_on', note=note_number, velocity=64, time=0))
                    for n in eval(note):
                        note_number = NoteToMidi(n)
                        track.append(Message('note_off', note=note_number, velocity=64, time=int(duration * 240)))  # 480 ticks per beat for 4/4 time signature  
                else:
                    note_number = NoteToMidi(note)
                    if note_number:
                        track.append(Message('note_on', note=note_number, velocity=64, time=0))
                        track.append(Message('note_off', note=note_number, velocity=64, time=int(duration * 240)))  # 480 ticks per beat for 4/4 time signature

    track.append(MetaMessage('end_of_track'))

    mid.save(name)