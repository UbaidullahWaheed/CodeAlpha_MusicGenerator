import customtkinter as ctk
import threading
import os

class GenerateTab:
    def __init__(self, parent):
        self.parent = parent
        self.is_generating = False
        self.build_ui()

    def build_ui(self):
        scroll = ctk.CTkScrollableFrame(self.parent, width=800, height=480)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            scroll,
            text="Generate AI Music",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            scroll,
            text="Adjust settings and generate a new music piece",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 15))

        # ── Settings Frame ────────────────────────────
        settings = ctk.CTkFrame(scroll)
        settings.pack(padx=30, pady=10, fill="x")

        # Notes Length
        ctk.CTkLabel(
            settings,
            text="Notes to Generate:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=20, pady=12, sticky="w")

        self.length_slider = ctk.CTkSlider(
            settings, from_=50, to=500, number_of_steps=45
        )
        self.length_slider.set(200)
        self.length_slider.grid(row=0, column=1, padx=20, pady=12)

        self.length_label = ctk.CTkLabel(
            settings, text="200 notes",
            font=ctk.CTkFont(size=12)
        )
        self.length_label.grid(row=0, column=2, padx=10)
        self.length_slider.configure(
            command=lambda v: self.length_label.configure(text=f"{int(v)} notes")
        )

        # Temperature
        ctk.CTkLabel(
            settings,
            text="Creativity:",
            font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, padx=20, pady=12, sticky="w")

        self.temp_slider = ctk.CTkSlider(
            settings, from_=0.1, to=2.0, number_of_steps=19
        )
        self.temp_slider.set(1.0)
        self.temp_slider.grid(row=1, column=1, padx=20, pady=12)

        self.temp_label = ctk.CTkLabel(
            settings, text="1.0",
            font=ctk.CTkFont(size=12)
        )
        self.temp_label.grid(row=1, column=2, padx=10)
        self.temp_slider.configure(
            command=lambda v: self.temp_label.configure(text=f"{v:.1f}")
        )

        # BPM
        ctk.CTkLabel(
            settings,
            text="BPM (Tempo):",
            font=ctk.CTkFont(size=13)
        ).grid(row=2, column=0, padx=20, pady=12, sticky="w")

        self.bpm_slider = ctk.CTkSlider(
            settings, from_=60, to=200, number_of_steps=28
        )
        self.bpm_slider.set(120)
        self.bpm_slider.grid(row=2, column=1, padx=20, pady=12)

        self.bpm_label = ctk.CTkLabel(
            settings, text="120 BPM",
            font=ctk.CTkFont(size=12)
        )
        self.bpm_label.grid(row=2, column=2, padx=10)
        self.bpm_slider.configure(
            command=lambda v: self.bpm_label.configure(text=f"{int(v)} BPM")
        )

        # Instrument
        ctk.CTkLabel(
            settings,
            text="Instrument:",
            font=ctk.CTkFont(size=13)
        ).grid(row=3, column=0, padx=20, pady=12, sticky="w")

        self.instrument_var = ctk.StringVar(value="Acoustic Grand Piano")
        ctk.CTkOptionMenu(
            settings,
            variable=self.instrument_var,
            values=[
                "Acoustic Grand Piano",
                "Electric Piano",
                "Violin",
                "Acoustic Guitar",
                "Flute",
                "Cello",
                "Vibraphone",
                "Choir Aahs"
            ],
            width=250
        ).grid(row=3, column=1, padx=20, pady=12)

        # Genre
        ctk.CTkLabel(
            settings,
            text="Genre Style:",
            font=ctk.CTkFont(size=13)
        ).grid(row=4, column=0, padx=20, pady=12, sticky="w")

        self.genre_var = ctk.StringVar(value="Classical")
        ctk.CTkOptionMenu(
            settings,
            variable=self.genre_var,
            values=["Classical", "Jazz", "Ambient", "Pop", "Cinematic"],
            width=250
        ).grid(row=4, column=1, padx=20, pady=12)

        # Key/Scale
        ctk.CTkLabel(
            settings,
            text="Key / Scale:",
            font=ctk.CTkFont(size=13)
        ).grid(row=5, column=0, padx=20, pady=12, sticky="w")

        self.key_var = ctk.StringVar(value="C Major")
        ctk.CTkOptionMenu(
            settings,
            variable=self.key_var,
            values=[
                "C Major", "G Major", "D Major", "F Major",
                "A Minor", "E Minor", "D Minor", "B Minor"
            ],
            width=250
        ).grid(row=5, column=1, padx=20, pady=12)

        # Output filename
        ctk.CTkLabel(
            settings,
            text="Output Filename:",
            font=ctk.CTkFont(size=13)
        ).grid(row=6, column=0, padx=20, pady=12, sticky="w")

        self.filename_var = ctk.StringVar(value="generated")
        ctk.CTkEntry(
            settings,
            textvariable=self.filename_var,
            width=200
        ).grid(row=6, column=1, padx=20, pady=12)

        ctk.CTkLabel(
            settings, text=".mid",
            font=ctk.CTkFont(size=12)
        ).grid(row=6, column=2, padx=5)

        # ── Status & Progress ─────────────────────────
        self.status_label = ctk.CTkLabel(
            scroll,
            text="Ready to generate...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            scroll, width=700, mode="indeterminate"
        )
        self.progress.pack(pady=5)

        # ── Buttons ───────────────────────────────────
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(pady=15)

        self.gen_btn = ctk.CTkButton(
            btn_frame,
            text="🎼 Generate Music",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            width=200,
            command=self.generate
        )
        self.gen_btn.grid(row=0, column=0, padx=10)

        # ── Output Path Label ─────────────────────────
        self.output_label = ctk.CTkLabel(
            scroll,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.output_label.pack(pady=5)

    # ── Instrument name to MIDI program number ────────
    def get_instrument_program(self):
        mapping = {
            "Acoustic Grand Piano": 0,
            "Electric Piano": 4,
            "Violin": 40,
            "Acoustic Guitar": 25,
            "Flute": 73,
            "Cello": 42,
            "Vibraphone": 11,
            "Choir Aahs": 52
        }
        return mapping.get(self.instrument_var.get(), 0)

    def generate(self):
        if self.is_generating:
            return

        self.is_generating = True
        self.gen_btn.configure(text="⏳ Generating...", state="disabled")
        self.progress.start()
        self.status_label.configure(
            text="🎼 Generating music...", text_color="gray"
        )

        length   = int(self.length_slider.get())
        temp     = float(self.temp_slider.get())
        bpm      = int(self.bpm_slider.get())
        program  = self.get_instrument_program()
        filename = self.filename_var.get().strip() or "generated"
        out_path = f"output/{filename}.mid"

        def run():
            try:
                import sys
                sys.path.insert(0, ".")
                from model.generate import generate_music
                path = generate_music(
                    output_path=out_path,
                    length=length,
                    temperature=temp,
                    bpm=bpm,
                    instrument_program=program
                )
                self.status_label.configure(
                    text="✅ Music Generated Successfully!",
                    text_color="green"
                )
                self.output_label.configure(
                    text=f"📁 Saved to: {os.path.abspath(path)}"
                )
            except Exception as e:
                self.status_label.configure(
                    text=f"❌ Error: {str(e)}",
                    text_color="red"
                )
            finally:
                self.is_generating = False
                self.progress.stop()
                self.gen_btn.configure(
                    text="🎼 Generate Music",
                    state="normal"
                )

        thread = threading.Thread(target=run, daemon=True)
        thread.start()