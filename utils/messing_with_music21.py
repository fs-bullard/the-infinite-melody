import music21
import os
mus = music21.converter.parse(os.getcwd() + '/Zeb/gnossie4.mid')
print(mus)
import pdb
pdb.set_trace()

music21.stream.Part.measures
music21.stream.Measure
music21.metadata.Metadata
music21.meter.TimeSignature
music21.tempo.MetronomeMark
music21.note.Note
music21.duration.Duration
music21.note.Rest
music21.pitch.Pitch
music21.chord.Chord