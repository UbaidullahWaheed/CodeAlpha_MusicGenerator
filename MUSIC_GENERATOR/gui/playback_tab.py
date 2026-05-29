import customtkinter as ctk
import pygame
import os
import glob
import tkinter as tk
import math

class PlaybackTab:
    def __init__(self, parent):
        self.parent = parent
        self.current_file = None
        self.is_playing = False
        self.wave_animation_id = None
        pygame.mixer.init()
        self.build_ui()

    def build_ui(self):
        scroll = ctk.CTkScrollableFrame(self.parent, width=800, height=480)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # ── Title ─────────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="🎵 Playback & Export",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            scroll,
            text="Play your generated MIDI files",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 15))

        # ── File Selection ────────────────────────────
        file_frame = ctk.CTkFrame(scroll)
        file_frame.pack(padx=30, pady=10, fill="x")

        ctk.CTkLabel(
            file_frame,
            text="Select MIDI File:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.file_var = ctk.StringVar(value="No file selected")
        self.file_menu = ctk.CTkOptionMenu(
            file_frame,
            variable=self.file_var,
            values=self.get_midi_files(),
            width=400
        )
        self.file_menu.grid(row=0, column=1, padx=20, pady=15)

        ctk.CTkButton(
            file_frame,
            text="🔄 Refresh",
            width=100,
            command=self.refresh_files
        ).grid(row=0, column=2, padx=10, pady=15)

        # ── Waveform Visualizer ───────────────────────
        ctk.CTkLabel(
            scroll,
            text="🎵 Waveform Visualizer",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 5))

        self.wave_canvas = tk.Canvas(
            scroll,
            width=700, height=100,
            bg="#0a0a1a",
            highlightthickness=1,
            highlightbackground="#1a1a3a"
        )
        self.wave_canvas.pack(pady=5)
        self._draw_flat_wave()

        # ── Now Playing ───────────────────────────────
        self.now_playing = ctk.CTkLabel(
            scroll,
            text="No file playing",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.now_playing.pack(pady=10)

        # ── Playback Controls ─────────────────────────
        controls = ctk.CTkFrame(scroll, fg_color="transparent")
        controls.pack(pady=10)

        self.play_btn = ctk.CTkButton(
            controls,
            text="▶️ Play",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150, height=45,
            command=self.play
        )
        self.play_btn.grid(row=0, column=0, padx=15, pady=10)

        self.stop_btn = ctk.CTkButton(
            controls,
            text="⏹ Stop",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150, height=45,
            fg_color="gray",
            command=self.stop
        )
        self.stop_btn.grid(row=0, column=1, padx=15, pady=10)

        # ── Export Frame ──────────────────────────────
        export_frame = ctk.CTkFrame(scroll)
        export_frame.pack(padx=30, pady=15, fill="x")

        ctk.CTkLabel(
            export_frame,
            text="Export Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=3, padx=20, pady=10)

        ctk.CTkButton(
            export_frame,
            text="📁 Open Output Folder",
            font=ctk.CTkFont(size=13),
            width=180, height=40,
            fg_color="transparent",
            border_width=2,
            command=self.open_folder
        ).grid(row=1, column=0, padx=15, pady=10)

        ctk.CTkButton(
            export_frame,
            text="📋 Copy File Path",
            font=ctk.CTkFont(size=13),
            width=180, height=40,
            fg_color="transparent",
            border_width=2,
            command=self.copy_path
        ).grid(row=1, column=1, padx=15, pady=10)

        ctk.CTkButton(
            export_frame,
            text="🗑️ Delete File",
            font=ctk.CTkFont(size=13),
            width=180, height=40,
            fg_color="transparent",
            border_width=2,
            hover_color="darkred",
            command=self.delete_file
        ).grid(row=1, column=2, padx=15, pady=10)

        # ── Status ────────────────────────────────────
        self.status_label = ctk.CTkLabel(
            scroll,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(pady=5)

    # ── Waveform Animation ────────────────────────────
    def _draw_flat_wave(self):
        self.wave_canvas.delete("all")
        w, h = 700, 100
        self.wave_canvas.create_line(
            0, h//2, w, h//2,
            fill="#1a1a4a", width=2
        )

    def _animate_wave(self, frame=0):
        if not self.is_playing:
            self._draw_flat_wave()
            return

        self.wave_canvas.delete("all")
        w, h = 700, 100
        cx = h // 2
        points = []

        for x in range(0, w, 3):
            freq1 = 0.03
            freq2 = 0.07
            freq3 = 0.015
            amp1  = 25 * math.sin(frame * 0.05)
            amp2  = 15 * math.cos(frame * 0.03)
            amp3  = 10

            y = cx + amp1 * math.sin(freq1 * x + frame * 0.1) \
                   + amp2 * math.sin(freq2 * x - frame * 0.08) \
                   + amp3 * math.sin(freq3 * x + frame * 0.05)
            points.extend([x, y])

        if len(points) >= 4:
            # Glow effect
            self.wave_canvas.create_line(
                points, fill="#1a1a6a", width=5, smooth=True
            )
            self.wave_canvas.create_line(
                points, fill="#3333aa", width=3, smooth=True
            )
            self.wave_canvas.create_line(
                points, fill="#6666ff", width=2, smooth=True
            )

        self.wave_animation_id = self.wave_canvas.after(
            30, self._animate_wave, frame + 1
        )

    # ── File Helpers ──────────────────────────────────
    def get_midi_files(self):
        files = glob.glob("output/*.mid")
        return files if files else ["No MIDI files found"]

    def refresh_files(self):
        files = self.get_midi_files()
        self.file_menu.configure(values=files)
        self.file_var.set(files[0])
        self.status_label.configure(text="🔄 File list refreshed!")

    # ── Playback Controls ─────────────────────────────
    def play(self):
        selected = self.file_var.get()
        if not os.path.exists(selected):
            self.status_label.configure(
                text="❌ File not found! Generate music first.",
                text_color="red"
            )
            return
        try:
            pygame.mixer.music.load(selected)
            pygame.mixer.music.play()
            self.is_playing = True
            self.now_playing.configure(
                text=f"🎵 Now Playing: {os.path.basename(selected)}",
                text_color="green"
            )
            self.play_btn.configure(text="▶️ Playing...")
            self.status_label.configure(
                text="Playing...", text_color="green"
            )
            self._animate_wave()
        except Exception as e:
            self.status_label.configure(
                text=f"❌ Error: {str(e)}", text_color="red"
            )

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_btn.configure(text="▶️ Play")
        self.now_playing.configure(text="Stopped", text_color="gray")
        self.status_label.configure(text="⏹ Stopped")
        self._draw_flat_wave()

    # ── Export Controls ───────────────────────────────
    def open_folder(self):
        os.startfile(os.path.abspath("output"))

    def copy_path(self):
        selected = self.file_var.get()
        self.wave_canvas.clipboard_clear()
        self.wave_canvas.clipboard_append(os.path.abspath(selected))
        self.status_label.configure(
            text="✅ Path copied to clipboard!", text_color="green"
        )

    def delete_file(self):
        selected = self.file_var.get()
        if os.path.exists(selected):
            os.remove(selected)
            self.status_label.configure(
                text="🗑️ File deleted!", text_color="orange"
            )
            self.refresh_files()
        else:
            self.status_label.configure(
                text="❌ File not found!", text_color="red"
            )