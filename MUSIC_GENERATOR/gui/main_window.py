import customtkinter as ctk
import tkinter as tk
import time
import threading

# ─── THEME SETTINGS ───────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── SPLASH SCREEN ────────────────────────────────────
class SplashScreen(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("")
        self.geometry("500x300")
        self.resizable(False, False)
        self.overrideredirect(True)

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 150
        self.geometry(f"500x300+{x}+{y}")

        # Background
        self.configure(fg_color="#0a0a1a")

        # Logo
        ctk.CTkLabel(
            self,
            text="🎵",
            font=ctk.CTkFont(size=60)
        ).pack(pady=(40, 5))

        ctk.CTkLabel(
            self,
            text="AI Music Generator",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#6666ff"
        ).pack(pady=5)

        ctk.CTkLabel(
            self,
            text="Powered by LSTM Deep Learning",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=5)

        ctk.CTkLabel(
            self,
            text="CodeAlpha Internship Project",
            font=ctk.CTkFont(size=11),
            text_color="#444466"
        ).pack(pady=5)

        # Loading bar
        self.progress = ctk.CTkProgressBar(
            self, width=400, mode="indeterminate"
        )
        self.progress.pack(pady=20)
        self.progress.start()

        ctk.CTkLabel(
            self,
            text="Loading...",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack()

# ─── MAIN WINDOW ──────────────────────────────────────
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎵 AI Music Generator — CodeAlpha")
        self.geometry("900x750")
        self.resizable(False, False)
        self.withdraw()  # Hide main window during splash

        # Show splash
        self.splash = SplashScreen()
        self.after(3000, self._close_splash)

    def _close_splash(self):
        self.splash.destroy()
        self.deiconify()  # Show main window
        self._build_ui()

    def _build_ui(self):
        # ── Header Frame ──────────────────────────────
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 0))

        ctk.CTkLabel(
            header_frame,
            text="🎵 AI Music Generator",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left", padx=20)

        # Theme Toggle
        self.theme_mode = ctk.StringVar(value="dark")
        theme_btn = ctk.CTkButton(
            header_frame,
            text="☀️ Light Mode",
            width=130,
            height=35,
            fg_color="transparent",
            border_width=2,
            command=self.toggle_theme
        )
        theme_btn.pack(side="right", padx=20)
        self.theme_btn = theme_btn

        ctk.CTkLabel(
            self,
            text="Powered by LSTM Deep Learning • CodeAlpha Internship",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=(0, 15))

        # ── Tab View ──────────────────────────────────
        self.tabview = ctk.CTkTabview(self, width=860, height=580)
        self.tabview.pack(padx=20, pady=10)

        self.tabview.add("🎓  Train Model")
        self.tabview.add("🎼  Generate Music")
        self.tabview.add("▶️  Playback")

        # ── Load Tabs ─────────────────────────────────
        from gui.train_tab import TrainTab
        from gui.generate_tab import GenerateTab
        from gui.playback_tab import PlaybackTab

        self.train_tab    = TrainTab(self.tabview.tab("🎓  Train Model"))
        self.generate_tab = GenerateTab(self.tabview.tab("🎼  Generate Music"))
        self.playback_tab = PlaybackTab(self.tabview.tab("▶️  Playback"))

        # ── Footer ────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="CodeAlpha AI Internship  •  Music Generation with LSTM  •  2026",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(5, 10))

    def toggle_theme(self):
        if self.theme_mode.get() == "dark":
            ctk.set_appearance_mode("light")
            self.theme_mode.set("light")
            self.theme_btn.configure(text="🌙 Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_mode.set("dark")
            self.theme_btn.configure(text="☀️ Light Mode")

def launch():
    app = MainWindow()
    app.mainloop()