import threading
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser
import comtypes
from audio import AudioController
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item


class AudioLockerTray:

    def __init__(self, max_volume, check_interval, unlock_time, password):
        self.max_volume = max_volume
        self.check_interval = check_interval
        self.unlock_time = unlock_time
        self.password = password

        self.audio = AudioController()
        self.locked = True
        self.unlocked_until = 0
        self.running = True

        self.icon_locked = self._create_image("red")
        self.icon_unlocked = self._create_image("green")

        menu = (
            item("Status: BLOQUEADO", lambda: None, enabled=False),
            item("Desbloquear Áudio", self._on_unlock_click),
            item("Ajuda", self._open_website),
            item("Sair", self._on_exit_click),
        )

        self.tray_icon = pystray.Icon(
            "AudioLocker", self.icon_locked, "AudioLocker - Bloqueado", menu
        )

    def _create_image(self, color):
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=color)
        return image

    def _open_website(self, icon, item):
        webbrowser.open("https://klebersilva.dev.br/audiolocker")

    def _update_tray_menu(self):
        if self.locked:
            status_text = "Status: BLOQUEADO"
            icon = self.icon_locked
            title = "AudioLocker - Bloqueado"
        else:
            remaining = max(0, int(self.unlocked_until - time.time()))
            mins, secs = divmod(remaining, 60)
            status_text = f"Status: LIBERADO ({mins:02d}:{secs:02d})"
            icon = self.icon_unlocked
            title = f"AudioLocker - Liberado ({mins:02d}:{secs:02d})"

        menu = (
            item(status_text, lambda: None, enabled=False),
            item(
                "Desbloquear Áudio" if self.locked else "Bloquear Agora",
                self._toggle_lock,
            ),
            item("Ajuda", self._open_website),
            item("Sair", self._on_exit_click),
        )

        self.tray_icon.menu = menu
        self.tray_icon.icon = icon
        self.tray_icon.title = title

    def _toggle_lock(self, icon, item):
        if self.locked:
            self._on_unlock_click(icon, item)
        else:
            self.lock()

    def _on_unlock_click(self, icon, item):
        threading.Thread(
            target=lambda: self._show_password_window(action_type="unlock"),
            daemon=True,
        ).start()

    def _on_exit_click(self, icon, item):
        threading.Thread(
            target=lambda: self._show_password_window(action_type="exit"),
            daemon=True,
        ).start()

    def _show_password_window(self, action_type="unlock"):
        """Abre janela para validação de senha tanto para Desbloquear quanto para Sair."""
        dialog = tk.Tk()
        dialog.title("AudioLocker")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.configure(bg="#2b2b2b")

        dialog.eval("tk::PlaceWindow . center")

        title_text = (
            "Senha para DESBLOQUEAR o Áudio:"
            if action_type == "unlock"
            else "Senha para SAIR do app:"
        )

        label = tk.Label(
            dialog,
            text=title_text,
            fg="white",
            bg="#2b2b2b",
            font=("Segoe UI", 10, "bold"),
        )
        label.pack(pady=(15, 5))

        entry = tk.Entry(
            dialog, show="•", font=("Segoe UI", 12), justify="center"
        )
        entry.pack(pady=5, padx=20, fill="x")
        entry.focus_force()

        def validate():
            pwd = entry.get()
            if pwd == self.password:
                dialog.destroy()
                if action_type == "unlock":
                    self.unlock()
                elif action_type == "exit":
                    self.running = False
                    self.tray_icon.stop()
            else:
                entry.delete(0, tk.END)
                messagebox.showerror(
                    "Erro", "Senha incorreta!", parent=dialog
                )

        btn_text = "Desbloquear" if action_type == "unlock" else "Encerrar App"
        btn_color = "#007acc" if action_type == "unlock" else "#d9534f"

        btn = tk.Button(
            dialog,
            text=btn_text,
            command=validate,
            bg=btn_color,
            fg="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
        )
        btn.pack(pady=10, ipadx=10)

        entry.bind("<Return>", lambda event: validate())

        dialog.mainloop()

    def lock(self):
        self.locked = True
        self._update_tray_menu()

    def unlock(self):
        self.locked = False
        self.unlocked_until = time.time() + self.unlock_time
        self._update_tray_menu()

    def _audio_loop(self):
        # Inicializa o COM da Microsoft para a thread do loop ter acesso aos controles de áudio
        try:
            comtypes.CoInitialize()
        except Exception:
            pass

        while self.running:
            if not self.locked:
                if time.time() >= self.unlocked_until:
                    self.lock()
                else:
                    self._update_tray_menu()
            else:
                self.audio.enforce_limit(self.max_volume)

            time.sleep(self.check_interval)

    def run(self):
        audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        audio_thread.start()
        self.tray_icon.run()