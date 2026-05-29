# 🎵 AI Music Generator — CodeAlpha Internship

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red?style=for-the-badge&logo=pytorch)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A professional AI-powered music generation desktop application built with LSTM Deep Learning**

*CodeAlpha AI Internship — Task 3*

</div>

---

## 📌 About The Project

AI Music Generator is a fully GUI-based desktop application that uses **Long Short-Term Memory (LSTM)** neural networks to learn music patterns from the MAESTRO dataset and generate original music compositions. The app allows users to train the AI model, generate music with customizable settings, and play it back — all from a beautiful, modern interface.

This project was built as part of the **CodeAlpha AI Internship Program** to demonstrate real-world application of deep learning in creative AI.

---

## 🎬 Demo

> Train the model → Generate music → Play it back instantly!

The app features:
- 🎓 **Train Tab** — Train LSTM model with live loss graph
- 🎼 **Generate Tab** — Generate music with custom settings
- ▶️ **Playback Tab** — Play generated music with waveform visualizer

---

## ✨ Features

### 🤖 AI & Machine Learning
- LSTM-based deep learning model built with **PyTorch**
- Trained on **MAESTRO Dataset** (1,276 professional piano MIDI files)
- Extracts and learns note sequences and chord patterns
- Generates completely original music compositions

### 🎨 Professional GUI
- Modern dark/light theme with **CustomTkinter**
- Animated **splash screen** on launch
- **Dark/Light mode toggle**
- Scrollable, responsive layout

### 🎵 Music Generation Controls
- **Notes to Generate** — slider (50 to 500 notes)
- **Creativity (Temperature)** — controls randomness (0.1 to 2.0)
- **BPM (Tempo)** — slider (60 to 200 BPM)
- **Instrument Selector** — Piano, Violin, Guitar, Flute, Cello, Choir and more
- **Genre Style** — Classical, Jazz, Ambient, Pop, Cinematic
- **Key / Scale** — C Major, A Minor, D Minor and more

### 📊 Training Dashboard
- Live **loss graph** updates during training
- Training progress bar with epoch counter
- Detailed training logs

### ▶️ Playback & Export
- Animated **waveform visualizer** while playing
- Play / Stop controls
- Copy file path to clipboard
- Open output folder directly
- Delete generated files

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.14** | Core programming language |
| **PyTorch** | LSTM model training & inference |
| **music21** | MIDI parsing and note extraction |
| **pretty_midi** | MIDI file generation |
| **CustomTkinter** | Modern GUI framework |
| **pygame-ce** | MIDI playback |
| **NumPy** | Numerical computations |
| **Pillow** | Image processing |

---

## 📁 Project Structure

```
CodeAlpha_MusicGenerator/
│
├── 📁 gui/
│   ├── main_window.py      # Main app window + splash screen
│   ├── train_tab.py        # Training UI + loss graph
│   ├── generate_tab.py     # Music generation UI
│   └── playback_tab.py     # Playback + waveform visualizer
│
├── 📁 model/
│   ├── train.py            # LSTM model + training logic
│   ├── generate.py         # Music generation logic
│   ├── music_model.pth     # Saved trained model (after training)
│   └── notes.pkl           # Extracted notes cache
│
├── 📁 data/
│   ├── 📁 2004/            # MAESTRO MIDI files by year
│   ├── 📁 2006/
│   ├── 📁 2008/
│   └── ...
│
├── 📁 output/              # Generated MIDI files saved here
├── App.py                  # Entry point — run this!
└── requirements.txt        # All dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10, 3.11, or 3.14
- pip package manager
- Windows / Mac / Linux

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YourUsername/CodeAlpha_MusicGenerator.git
cd CodeAlpha_MusicGenerator
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install torch music21 pretty_midi pygame-ce customtkinter pillow numpy
```

**4. Download MAESTRO Dataset**
- Go to: https://magenta.tensorflow.org/datasets/maestro
- Download **MIDI only** version (~57MB)
- Extract and place year folders (2004, 2006...) inside `data/`

**5. Run the app**
```bash
python App.py
```

---

## 🎮 How To Use

### Step 1 — Train The Model
1. Open the app → click **Train Model** tab
2. Set epochs (20 recommended) and MIDI files (10 recommended)
3. Click **🚀 Start Training**
4. Watch the live loss graph update
5. Wait for **"Training Complete!"** message

> ⚠️ Training is a one-time process. The model saves automatically.

### Step 2 — Generate Music
1. Click **Generate Music** tab
2. Adjust your settings:
   - Choose instrument, genre, key, BPM
   - Set creativity level
   - Enter output filename
3. Click **🎼 Generate Music**
4. Wait a few seconds for generation

### Step 3 — Play & Export
1. Click **Playback** tab
2. Click **🔄 Refresh** to load your file
3. Select your generated file
4. Click **▶️ Play** and enjoy the waveform visualizer!

---

## 🎵 Recommended Settings For Best Results

| Style | BPM | Creativity | Instrument | Key |
|---|---|---|---|---|
| Classical | 72 | 0.7 | Acoustic Grand Piano | A Minor |
| Drama OST | 65 | 0.7 | Violin | D Minor |
| Jazz | 110 | 1.3 | Vibraphone | D Minor |
| Ambient | 60 | 0.9 | Choir Aahs | C Major |
| Cinematic | 85 | 1.0 | Violin | E Minor |
| Pop | 128 | 1.2 | Electric Piano | G Major |

---

## 📸 Screenshots

><img width="649" height="505" alt="image" src="https://github.com/user-attachments/assets/4106a600-0a7d-4cc9-829c-10ecb56eea0d" />


---

## 🤖 How The AI Works

```
MIDI Files → Note Extraction → Sequence Preparation
     ↓
LSTM Neural Network Training
     ↓
Pattern Learning (notes, chords, rhythms)
     ↓
Music Generation (new sequences)
     ↓
MIDI File Output
```

The LSTM model learns the statistical patterns in music — which notes typically follow which other notes, chord progressions, and musical phrases. During generation, it uses these learned patterns to create new, original compositions.

---

## 👨‍💻 Developer

**Ubaidullah Waheed**
- 🎓 CodeAlpha AI Internship
- 💼 LinkedIn: [https://www.linkedin.com/in/ubaidullah-waheed-a119ba383/]
- 🐙 GitHub: [https://github.com/UbaidullahWaheed]
  

---

## 🏢 About CodeAlpha

CodeAlpha is a leading software development company dedicated to driving innovation and excellence across emerging technologies. This project was built as part of their AI internship program.

🌐 Website: www.codealpha.tech

---

## 📄 License

This project is licensed under the MIT License — feel free to use and modify it!

---

<div align="center">

⭐ **If you found this project helpful, please give it a star!** ⭐

*Built with ❤️ by Ubaidullah Waheed — CodeAlpha AI Internship 2026*

</div>
