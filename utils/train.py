import torch
import numpy as np
import torch.utils.data as data
import time
import torch.nn as nn
from torch.autograd import Variable
import os

def split_sequences(inp, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(inp) - seq_length):
        seq_in = inp[i:i + seq_length]
        seq_out = inp[i + seq_length]
        dataX.append(seq_in)
        dataY.append(seq_out)
    return data.TensorDataset(torch.tensor(np.array(dataX), dtype=torch.int32), torch.tensor(np.array(dataY), dtype=torch.int32))

class MusicRNN(torch.nn.Module):
    def __init__(self, input_size, output_size, sequence_length, hidden_size, num_layers=1, dropout=0.2):
        super(MusicRNN, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        
        self.embeddings = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.LSTM(hidden_size, hidden_size, num_layers)
        self.drop = nn.Dropout(p=dropout)
        self.out = nn.Linear(sequence_length*self.hidden_size, self.output_size)
        
    def init_hidden(self, device, batch_size):
        self.hidden = (Variable(torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)), Variable(torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)))
        
    def forward(self, seq):
        batch_size, seq_len = seq.size()
        embeds = self.embeddings(seq.view(1, -1))
        rnn_out, self.hidden = self.rnn(embeds.view(seq_len,batch_size,self.hidden_size), self.hidden)
        rnn_out = self.drop(rnn_out)
        output = self.out(rnn_out.view(batch_size,-1))
        return output


if __name__ == "__main__":

    dataset = np.load("dataset2.npy", allow_pickle=True)
    
    d = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(d)
    print("Running on: "+d)

    epochs = 50
    batch_size = 32
    n_timesteps = 300 # this is number of timesteps

    # convert dataset into input/output
    dataset = split_sequences(dataset, n_timesteps)
    loader = data.DataLoader(dataset, batch_size=batch_size)

    # create NN
    note_model = MusicRNN(51, 51, n_timesteps, hidden_size=300).to(device)
    # note_model = torch.load("note_model.pth").to(device)
    note_criterion = nn.CrossEntropyLoss()
    note_optimizer = torch.optim.Adam(note_model.parameters(), lr=0.001)
    note_model.train()

    duration_model = MusicRNN(12, 12, n_timesteps, hidden_size=1000).to(device)
    # duration_model = torch.load("duration_model.pth").to(device)
    duration_criterion = nn.CrossEntropyLoss()
    duration_optimizer = torch.optim.Adam(duration_model.parameters(), lr=0.001)
    duration_model.train()
    
    for t in range(epochs):
        stime = time.time()
        stime2 = time.time()
        for X, y in loader:
            if time.time() - stime2 > 3600:
                torch.save(note_model, "note_model.pth")
                torch.save(duration_model, "duration_model.pth")
                stime2 = time.time()
            noteX, durationX = X[:,:,0].to(device), X[:,:,1].to(device)
            noteY, durationY = y[:,0].to(device), y[:,1].to(device)

            if noteX.size()[0] == batch_size:
                note_model.init_hidden(device, batch_size)
                duration_model.init_hidden(device, batch_size)

                note_output = note_model(noteX)
                duration_output = duration_model(durationX)
                
                note_loss = note_criterion(note_output, noteY.long())
                duration_loss = duration_criterion(duration_output, durationY.long())
                
                note_optimizer.zero_grad()
                note_loss.backward()
                note_optimizer.step()

                duration_optimizer.zero_grad()
                duration_loss.backward()
                duration_optimizer.step()
        
        print('Epoch : ' , t+1 , 'note loss : ' , note_loss.item(), 'duration loss : ' , duration_loss.item(), ' time taken: ', time.time()-stime)
        torch.save(note_model, "note_model"+str(t+1)+".pth")
        torch.save(duration_model, "duration_model"+str(t+1)+".pth")