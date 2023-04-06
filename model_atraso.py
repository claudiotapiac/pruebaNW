import torch.nn as nn

class Autoencoder(nn.Module):
    def __init__(self, input_size):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, input_size),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# Definir el modelo de clasificación
class Classifier(nn.Module):
    def __init__(self,input_size):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_size, input_size)
        self.fc2 = nn.Linear(input_size, input_size)
        self.fc3 = nn.Linear(input_size, 1)
        self.sigmoid = nn.Sigmoid()
        self.ReLU = nn.ReLU()
        self.dropout = nn.Dropout(p=0.4)
    def forward(self, x):
        x = self.fc1(x)
        x = self.ReLU(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.ReLU(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

# Combinar los modelos en uno solo
class AutoencoderClassifier(nn.Module):
    def __init__(self,input_size):
        super(AutoencoderClassifier, self).__init__()
        self.autoencoder = Autoencoder(input_size)
        self.classifier = Classifier(input_size)

    def forward(self, x):
        x = self.autoencoder(x)
        x = self.classifier(x)
        return x