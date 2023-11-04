import torch
import numpy as np
from train import MultiFeatureRNN
import __main__
setattr(__main__, "MultiFeatureRNN", MultiFeatureRNN)

sequence = torch.tensor(np.random.rand(3,2), dtype=torch.float32)

model = torch.load("model.pth")
model.eval()
model.init_hidden(1)

print(sequence)

with torch.no_grad():
    while True:
        next_note = model(sequence.view(1,3,2))
        print(next_note.tolist()[0])
        ## send next_note to 
        sequence = torch.cat([sequence[1:], next_note])