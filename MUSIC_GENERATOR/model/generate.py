import pickle
import numpy as np
import torch
import torch.nn as nn
import pretty_midi

# ─── CONFIG ───────────────────────────────────────────
NOTES_PATH   = "model/notes.pkl"
MODEL_PATH   = "model/music_model.pth"
SEQUENCE_LEN = 100

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

# ─── LOAD MODEL ───────────────────────────────────────
def load_model():
    with open(NOTES_PATH, 'rb') as f:
        notes = pickle.load(f)

    unique      = sorted(set(notes))
    n_vocab     = len(unique)
    int_to_note = {i: n for i, n in enumerate(unique)}
    note_to_int = {n: i for i, n in enumerate(unique)}

    model = MusicLSTM(1, 256, n_vocab)
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()
    return model, notes, note_to_int, int_to_note, n_vocab

# ─── GENERATE NOTES ───────────────────────────────────
def generate_notes(model, notes, note_to_int, int_to_note,
                   n_vocab, length=200, temperature=1.0):
    start   = np.random.randint(0, len(notes) - SEQUENCE_LEN)
    pattern = [note_to_int[n] for n in notes[start:start + SEQUENCE_LEN]]
    output  = []

    for _ in range(length):
        x = np.array(pattern) / n_vocab
        x = torch.tensor(x, dtype=torch.float32).unsqueeze(0).unsqueeze(-1)

        with torch.no_grad():
            pred = model(x)
            pred = pred / temperature
            probs = torch.softmax(pred, dim=1).squeeze().numpy()

        idx = np.random.choice(len(probs), p=probs)
        output.append(int_to_note[idx])
        pattern.append(idx)
        pattern = pattern[1:]

    return output

# ─── CONVERT TO MIDI ──────────────────────────────────
def notes_to_midi(notes_list, output_path="output/generated.mid",
                  bpm=120, instrument_program=0):
    midi  = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    piano = pretty_midi.Instrument(program=instrument_program)

    current_time = 0.0
    beat_duration = 60.0 / bpm
    duration      = beat_duration * 0.5

    for n in notes_list:
        if '.' in n:  # chord
            for pitch_str in n.split('.'):
                try:
                    pitch = int(pitch_str) + 60
                    pitch = max(0, min(127, pitch))
                    note_obj = pretty_midi.Note(
                        velocity=90, pitch=pitch,
                        start=current_time,
                        end=current_time + duration
                    )
                    piano.notes.append(note_obj)
                except:
                    pass
        else:  # single note
            try:
                pitch = pretty_midi.note_name_to_number(n)
                pitch = max(0, min(127, pitch))
                note_obj = pretty_midi.Note(
                    velocity=90, pitch=pitch,
                    start=current_time,
                    end=current_time + duration
                )
                piano.notes.append(note_obj)
            except:
                pass
        current_time += duration

    midi.instruments.append(piano)
    midi.write(output_path)
    print(f"MIDI saved to {output_path}")
    return output_path

# ─── MAIN FUNCTION ────────────────────────────────────
def generate_music(output_path="output/generated.mid",
      length=200, temperature=1.0,
      bpm=120, instrument_program=0):
    model, notes, note_to_int, int_to_note, n_vocab = load_model()
    generated = generate_notes(
        model, notes, note_to_int,
        int_to_note, n_vocab, length, temperature
    )
    path = notes_to_midi(
        generated, output_path,
        bpm=bpm,
        instrument_program=instrument_program
    )
    return path

if __name__ == "__main__":
    generate_music()