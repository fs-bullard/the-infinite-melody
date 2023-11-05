import music21
import os
import csv

mus = music21.converter.parse(os.getcwd() + '/Zeb/gnossie4.mid')
note_list = []
total_q = 0
tempo = []

for part in mus:
    if type(part) == music21.stream.Part:
        piano = False
        for instrument in part[0]:
            if type(instrument) == music21.instrument.Piano:
                piano = True
        
        if piano:
            for measure in part:
                if type(measure) == music21.stream.Measure:
                    for obj in measure:
                        if type(obj) == music21.tempo.MetronomeMark:
                            if note_list:
                                last_offset = note_list[-1][2]
                                change_in_offset = last_offset - tempo[-1][1]
                                tempo.append((obj.number * obj.referent.quarterLength,
                                              last_offset,
                                              round(tempo[-1][2] + change_in_offset*(60 / tempo[-1][0]), 2)))
                            else:
                                tempo.append((obj.number * obj.referent.quarterLength, 0, 0))
                        if type(obj) == music21.note.Note:
                            note_list.append([[obj.pitch.nameWithOctave], 
                                            round(obj.duration.quarterLength * (60 / tempo[-1][0]), 2), 
                                            total_q + obj.offset,
                                            round(tempo[-1][2] + (total_q + obj.offset - tempo[-1][1]) * (60 / tempo[-1][0]), 2)])
                        if type(obj) == music21.note.Rest:
                            note_list.append([obj.name, 
                                          round(obj.duration.quarterLength * (60 / tempo[-1][0]), 2), 
                                          total_q + obj.offset,
                                          round(tempo[-1][2] + (total_q + obj.offset - tempo[-1][1]) * (60 / tempo[-1][0]), 2)])
                        if type(obj) == music21.chord.Chord:
                            note_list.append([[p.nameWithOctave for p in obj.pitches],
                                              round(obj.duration.quarterLength * (60 / tempo[-1][0]), 2),
                                              total_q + obj.offset,
                                              round(tempo[-1][2] + (total_q + obj.offset - tempo[-1][1]) * (60 / tempo[-1][0]), 2)])
                if note_list:
                    total_q += measure.duration.quarterLength

notes = []
for note in note_list:
    notes.append([note[0], note[1]])

with open('test_no_time.csv', 'w', newline='') as f:
     
    write = csv.writer(f)
    write.writerows(notes)
