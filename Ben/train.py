import torch
import numpy as np
import torch.utils.data as data

def split_sequences(inp, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(inp) - seq_length):
        seq_in = inp[i:i + seq_length]
        seq_out = inp[i + seq_length]
        dataX.append(seq_in)
        dataY.append(seq_out)
    return data.TensorDataset(torch.tensor(dataX), torch.tensor(dataY))

class MultiFeatureRNN(torch.nn.Module):
    def __init__(self,n_features,seq_length):
        super(MultiFeatureRNN, self).__init__()
        self.n_features = n_features
        self.seq_len = seq_length
        self.n_hidden = 20 # number of hidden states
        self.n_layers = 1 # number of LSTM layers (stacked)
    
        self.l_lstm = torch.nn.LSTM(input_size = n_features, 
                                 hidden_size = self.n_hidden,
                                 num_layers = self.n_layers, 
                                 batch_first = True)
        self.l_linear = torch.nn.Linear(self.n_hidden*self.seq_len, 2)
        
    
    def init_hidden(self, batch_size):
        hidden_state = torch.zeros(self.n_layers,batch_size,self.n_hidden)
        cell_state = torch.zeros(self.n_layers,batch_size,self.n_hidden)
        self.hidden = (hidden_state, cell_state)
    
    
    def forward(self, x):
        batch_size, seq_len, _ = x.size()
        
        lstm_out, self.hidden = self.l_lstm(x,self.hidden)
        x = lstm_out.contiguous().view(batch_size,-1)
        return self.l_linear(x)

if __name__ == "__main__": 
    dataset = np.random.rand(1000, 2)

    epochs = 500
    batch_size = 16

    n_features = 2 # this is number of parallel inputs
    n_timesteps = 3 # this is number of timesteps

    # convert dataset into input/output
    dataset = split_sequences(dataset, n_timesteps)
    loader = data.DataLoader(dataset, batch_size=16)

    # create NN
    mv_net = MultiFeatureRNN(n_features,n_timesteps)
    criterion = torch.nn.MSELoss() # reduction='sum' created huge loss value
    optimizer = torch.optim.Adam(mv_net.parameters(), lr=1e-1)
    mv_net.train()
    for t in range(epochs):
        for X, y in loader: 
            
            x_batch = torch.tensor(X,dtype=torch.float32)    
            y_batch = torch.tensor(y,dtype=torch.float32)
            
            mv_net.init_hidden(x_batch.size(0))
            output = mv_net(x_batch)
            loss = criterion(output, y_batch)
            
            loss.backward()
            optimizer.step()        
            optimizer.zero_grad() 
        print('step : ' , t , 'loss : ' , loss.item())

    torch.save(mv_net, "model.pth")