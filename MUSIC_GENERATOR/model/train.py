import os
import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord
import torch
import torch.nn as nn

# ─── CONFIG ───────────────────────────────────────────
MIDI_PATH   = "data"
SEQUENCE_LEN = 100
MODEL_PATH  = "model/music_model.pth"
NOTES_PATH  = "model/notes.pkl"

# ─── PARSE MIDI FILES ─────────────────────────────────
def get_notes():
    notes = []
    files = glob.glob(os.path.join(MIDI_PATH, "**/*.midi"), recursive=True) + glob.glob(os.path.join(MIDI_PATH, "**/*.mid"), recursive=True)
    print(f"Found {len(files)} MIDI files")

    for i, file in enumerate(files[:10]):  # Use first 50 files for speed
        try:
            midi = converter.parse(file)
            print(f"Parsing file {i+1}/50: {os.path.basename(file)}")
            parts = instrument.partitionByInstrument(midi)
            elements = parts.parts[0].recurse() if parts else midi.flat.notes
            for element in elements:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Skipping {file}: {e}")

    with open(NOTES_PATH, 'wb') as f:
        pickle.dump(notes, f)
    print(f"Total notes extracted: {len(notes)}")
    return notes

# ─── PREPARE SEQUENCES ────────────────────────────────
def prepare_sequences(notes):
    unique = sorted(set(notes))
    note_to_int = {n: i for i, n in enumerate(unique)}
    n_vocab = len(unique)

    inputs, targets = [], []
    for i in range(len(notes) - SEQUENCE_LEN):
        seq_in  = notes[i:i + SEQUENCE_LEN]
        seq_out = notes[i + SEQUENCE_LEN]
        inputs.append([note_to_int[n] for n in seq_in])
        targets.append(note_to_int[seq_out])

    X = np.array(inputs) / n_vocab
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(targets, dtype=torch.long)
    return X, y, n_vocab, note_to_int

# ─── LSTM MODEL ───────────────────────────────────────
class MusicLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(MusicLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size,
                            num_layers=num_layers, batch_first=True, dropout=0.3)
        self.fc   = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# ─── TRAIN ────────────────────────────────────────────
def train_model(progress_callback=None):
    notes = get_notes()
    if len(notes) < SEQUENCE_LEN:
        print("Not enough notes found!")
        return

    X, y, n_vocab, _ = prepare_sequences(notes)
    model  = MusicLSTM(1, 256, n_vocab)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    EPOCHS     = 20
    BATCH_SIZE = 256

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for i in range(0, len(X), BATCH_SIZE):
            xb = X[i:i+BATCH_SIZE]
            yb = y[i:i+BATCH_SIZE]
            optimizer.zero_grad()
            output = model(xb)
            loss   = criterion(output, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / (len(X) // BATCH_SIZE)
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {avg_loss:.4f}")
        if progress_callback:
            progress_callback(epoch+1, EPOCHS, avg_loss)

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()