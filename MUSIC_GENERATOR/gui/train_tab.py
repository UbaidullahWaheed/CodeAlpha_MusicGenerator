import customtkinter as ctk
import threading
import tkinter as tk

class TrainTab:
    def __init__(self, parent):
        self.parent = parent
        self.is_training = False
        self.loss_values = []
        self.build_ui()

    def build_ui(self):
        scroll = ctk.CTkScrollableFrame(self.parent, width=800, height=480)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            scroll,
            text="Train Your AI Music Model",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            scroll,
            text="The model will learn music patterns from the MAESTRO dataset",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 15))

        # ── Settings Frame ────────────────────────────
        settings = ctk.CTkFrame(scroll)
        settings.pack(padx=30, pady=10, fill="x")

        ctk.CTkLabel(
            settings,
            text="Number of Epochs:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.epochs_var = ctk.StringVar(value="20")
        ctk.CTkEntry(
            settings,
            textvariable=self.epochs_var,
            width=100
        ).grid(row=0, column=1, padx=20, pady=15)

        ctk.CTkLabel(
            settings,
            text="MIDI Files to Use:",
            font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, padx=20, pady=15, sticky="w")

        self.files_var = ctk.StringVar(value="10")
        ctk.CTkEntry(
            settings,
            textvariable=self.files_var,
            width=100
        ).grid(row=1, column=1, padx=20, pady=15)

        # ── Progress Bar ──────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="Training Progress:",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(15, 5))

        self.progress = ctk.CTkProgressBar(scroll, width=700)
        self.progress.pack(pady=5)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            scroll,
            text="Ready to train...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(pady=5)

        # ── Loss Graph ────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="Training Loss Graph:",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 5))

        self.canvas = tk.Canvas(
            scroll,
            width=700, height=150,
            bg="#1a1a2e",
            highlightthickness=1,
            highlightbackground="#333366"
        )
        self.canvas.pack(pady=5)
        self.canvas.create_text(
            350, 75,
            text="Loss graph will appear during training...",
            fill="#666699",
            font=("Arial", 11)
        )

        # ── Log Box ───────────────────────────────────
        self.log_box = ctk.CTkTextbox(scroll, width=700, height=120)
        self.log_box.pack(pady=10)
        self.log_box.insert("end", "Training logs will appear here...\n")
        self.log_box.configure(state="disabled")

        # ── Train Button ──────────────────────────────
        self.train_btn = ctk.CTkButton(
            scroll,
            text="🚀 Start Training",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            width=200,
            command=self.start_training
        )
        self.train_btn.pack(pady=20)

    def draw_loss_graph(self):
        self.canvas.delete("all")
        if len(self.loss_values) < 2:
            return

        w, h = 700, 150
        pad = 30
        max_loss = max(self.loss_values)
        min_loss = min(self.loss_values)
        loss_range = max_loss - min_loss or 1

        # Grid lines
        for i in range(5):
            y = pad + (h - 2*pad) * i / 4
            self.canvas.create_line(
                pad, y, w-pad, y,
                fill="#333366", dash=(2,4)
            )

        # Loss line
        points = []
        for i, loss in enumerate(self.loss_values):
            x = pad + (w - 2*pad) * i / (len(self.loss_values) - 1)
            y = pad + (h - 2*pad) * (1 - (loss - min_loss) / loss_range)
            points.append((x, y))

        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0], points[i][1],
                points[i+1][0], points[i+1][1],
                fill="#4d79ff", width=2
            )

        # Dots
        for x, y in points:
            self.canvas.create_oval(
                x-3, y-3, x+3, y+3,
                fill="#7799ff", outline=""
            )

        # Labels
        self.canvas.create_text(
            pad, pad-10,
            text=f"{max_loss:.2f}",
            fill="#aaaacc", font=("Arial", 8)
        )
        self.canvas.create_text(
            pad, h-pad+10,
            text=f"{min_loss:.2f}",
            fill="#aaaacc", font=("Arial", 8)
        )
        self.canvas.create_text(
            350, h-10,
            text="Epochs",
            fill="#aaaacc", font=("Arial", 9)
        )

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_progress(self, epoch, total, loss):
        self.loss_values.append(loss)
        progress = epoch / total
        self.progress.set(progress)
        self.status_label.configure(
            text=f"Epoch {epoch}/{total} — Loss: {loss:.4f}"
        )
        self.log(f"✅ Epoch {epoch}/{total} — Loss: {loss:.4f}")
        self.draw_loss_graph()

    def start_training(self):
        if self.is_training:
            return

        self.is_training = True
        self.loss_values = []
        self.train_btn.configure(text="⏳ Training...", state="disabled")
        self.progress.set(0)
        self.log("🚀 Starting training...")

        def run():
            try:
                import sys
                sys.path.insert(0, ".")
                from model.train import train_model
                train_model(progress_callback=self.update_progress)
                self.log("🎉 Training complete! Model saved.")
                self.status_label.configure(
                    text="✅ Training Complete!",
                    text_color="green"
                )
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                self.status_label.configure(
                    text="❌ Training Failed",
                    text_color="red"
                )
            finally:
                self.is_training = False
                self.train_btn.configure(
                    text="🚀 Start Training",
                    state="normal"
                )

        thread = threading.Thread(target=run, daemon=True)
        thread.start()