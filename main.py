import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock

import torch
import numpy as np
import torch.nn as nn
import random
from torch.autograd import Variable
from os.path import join
import __main__

def generate_notes():
    class MusicRNN(torch.nn.Module):
        def __init__(self, input_size, output_size, sequence_length, hidden_size=150, num_layers=1, dropout=0.2):
            super(MusicRNN, self).__init__()
            self.input_size = input_size
            self.hidden_size = hidden_size
            self.output_size = output_size
            self.num_layers = num_layers
            
            self.embeddings = nn.Embedding(input_size, hidden_size)
            self.rnn = nn.LSTM(hidden_size, hidden_size, num_layers)
            self.drop = nn.Dropout(p=dropout)
            self.out = nn.Linear(sequence_length*self.hidden_size, self.output_size)
            
        def init_hidden(self, device, batch_size=100):
            self.hidden = (Variable(torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)), Variable(torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)))
            
        def forward(self, seq):
            batch_size, seq_len = seq.size()
            embeds = self.embeddings(seq.view(1, -1))
            rnn_out, self.hidden = self.rnn(embeds.view(seq_len,batch_size,150), self.hidden)
            rnn_out = self.drop(rnn_out)
            output = self.out(rnn_out.view(batch_size,-1))
            return output

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

    source_dir = "model_resources"

    mapping = np.load(join(source_dir,"mapping.npy"), allow_pickle=True).item()
    mapping = {v: k for k, v in mapping.items()}

    chords_consts = np.load(join(source_dir,"chords_consts.npy"), allow_pickle=True).item()
    chord_const = 25
    chords_vals = np.load(join(source_dir,"chords_vals.npy"), allow_pickle=True)

    note_model = torch.load(join(source_dir,"note_model.pth")).to(device)
    note_model.eval()
    note_model.init_hidden(device, 1)
    note_model.apply(deactivate_batchnorm)

    duration_model = torch.load(join(source_dir,"duration_model.pth")).to(device)
    duration_model.eval()
    duration_model.init_hidden(device, 1)
    duration_model.apply(deactivate_batchnorm)

    # Create seed
    sequence_len = 20
    dataset = np.load(join(source_dir,"dataset2.npy"), allow_pickle=True)
    idx = random.randint(0,len(dataset)-sequence_len-1)
    note_sequence, duration_sequence = [], []
    for i in range(idx, idx+sequence_len):
        note_sequence.append(dataset[i][0])
        duration_sequence.append(dataset[i][1])
    note_sequence, duration_sequence = torch.tensor(note_sequence, dtype=torch.int32), torch.tensor(duration_sequence, dtype=torch.int32)

    with torch.no_grad():
        prevk = []
        k = 4
        count = 1
        while True:
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

            socketio.emit('newnote', {'num': count, "note": newnote, "duration": round(duration)})
            count += 1

            note_sequence = torch.cat((note_sequence[1:], torch.tensor([sq_next_note])))
            duration_sequence = torch.cat((duration_sequence[1:], sq_next_duration))


# web socket
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"

# app.config['SECRET_KEY'] = 'key'
socketio = SocketIO(app, cors_allowed_origins='*', engineio_logger=True, logger=True)

@app.route('/')
def root():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(generate_notes)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, cors_allowed_origins="*")