import torch
import numpy as np
from train import MusicRNN
import torch.nn as nn
import random
from os.path import join
import __main__
from to_midi import toMIDI

setattr(__main__, "MusicRNN", MusicRNN)

def deactivate_batchnorm(m):
    if isinstance(m, nn.BatchNorm2d):
        m.reset_parameters()
        m.eval()
        with torch.no_grad():
            m.weight.fill_(1.0)
            m.bias.zero_()

sharp_to_flat = {
    "C#": "Db",
    "D#": "Eb",
    "E#": "F",
    "F#": "Gb",
    "G#": "Ab",
    "A#": "Bb",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

source_dir = "utils"

mapping = np.load(join(source_dir,"mapping.npy"), allow_pickle=True).item()
mapping = {v: k for k, v in mapping.items()}

chords_consts = np.load(join(source_dir,"chords_consts.npy"), allow_pickle=True).item()
chord_const = 25
chords_vals = np.load(join(source_dir,"chords_vals.npy"), allow_pickle=True)

note_model = torch.load(join(source_dir,"note_model8.pth")).to(device)
note_model.eval()
note_model.init_hidden(device, 1)
note_model.apply(deactivate_batchnorm)

duration_model = torch.load(join(source_dir,"duration_model8.pth")).to(device)
duration_model.eval()
duration_model.init_hidden(device, 1)
duration_model.apply(deactivate_batchnorm)

number_of_songs = 1
for track in range(number_of_songs):

    # Create seed
    sequence_len = 20
    dataset = np.load(join(source_dir,"dataset2.npy"), allow_pickle=True)
    idx = random.randint(0,len(dataset)-sequence_len-1)
    note_sequence, duration_sequence = [], []
    for i in range(idx, idx+sequence_len):
        note_sequence.append(dataset[i][0])
        duration_sequence.append(dataset[i][1])
    note_sequence, duration_sequence = torch.tensor(note_sequence, dtype=torch.int32), torch.tensor(duration_sequence, dtype=torch.int32)

    song, song2 = [], []

    with torch.no_grad():
        prevk = []
        k = 4
        for i in range(400):
            # next note
            next_note = note_model(note_sequence.to(device).view(1,sequence_len))
            probs = (1 / (1+ np.exp(-next_note)))[0]
            vals = [i for i in range(len(probs)) if i not in prevk]
            probs = np.array([x for i, x in enumerate(probs) if i not in prevk])
            probs[0] *= 0.3
            probs[-2] *= 0.3
            sq_next_note = np.random.choice(vals, p=probs/sum(probs).item())
            note = mapping[int(sq_next_note.item())]
            
            if len(prevk) == k:
                prevk = prevk[1:] + [sq_next_note]
            else:
                prevk.append(sq_next_note)

            # next duration
            next_duration = duration_model(duration_sequence.to(device).view(1,sequence_len))
            sq_next_duration = torch.argmax(next_duration, 1)
            duration = sq_next_duration.item() + 1

            if note == "rest":
                duration = np.clip(duration, 1, 4)

            # chords
            if note in chords_consts.keys() and random.uniform(0,1) < chord_const * chords_consts[note]:
                for a in sorted(chords_vals, key=lambda k: random.random()):
                    for b in a[0]:
                        if b == note:
                            note = a[0]
                            break
            
            # minus to b
            newnote = []
            if type(note) == str:
                note2 = [note]
            else:
                note2 = note
            for n in note2:
                if "-" in n:
                    n = n.replace("-", "b")
                if "#" in n:
                    n = sharp_to_flat[n[:2]] + n[2:]
                newnote.append(n)

            song.append([note, round(duration/4)])
            song2.append([newnote, round(duration/4)])

            note_sequence = torch.cat((note_sequence[1:], torch.tensor([sq_next_note])))
            duration_sequence = torch.cat((duration_sequence[1:], sq_next_duration))

    f = open("utils/songs/song"+str(track)+".txt", "w")
    f.write(str(song2))
    f.close()
    toMIDI(song, "utils/songs/song"+str(track)+".mid")