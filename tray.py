import hashlib
import threading
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser

from audio import AudioController
import comtypes
from config_wizard import run_edit_wizard
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item


def hash_password(password: str) -> str:
    """Gera o hash SHA-256 da senha digitada para validação."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


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
        self.warning_open = False

        self.icon_locked = self._create_image("red")
        self.icon_unlocked = self._create_image("green")

        menu = (
            item("Status: BLOQUEADO", lambda: None, enabled=False),
            item("Desbloquear Áudio", self._on_unlock_click),
            item("Configurações", self._on_config_click),
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
            item("Configurações", self._on_config_click),
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

    def _on_config_click(self, icon, item):
        threading.Thread(
            target=lambda: self._show_password_window(action_type="config"),
            daemon=True,
        ).start()

    def _on_exit_click(self, icon, item):
        threading.Thread(
            target=lambda: self._show_password_window(action_type="exit"),
            daemon=True,
        ).start()

    def _open_edit_wizard(self):
        """Abre a janela de edição passando os valores atuais e aplica as mudanças."""
        updated_config = run_edit_wizard(
            current_vol=self.max_volume,
            current_time=self.unlock_time,
            current_pwd_hash=self.password,
        )
        if updated_config:
            self.max_volume = updated_config["MAX_VOLUME"]
            self.unlock_time = updated_config["UNLOCK_TIME"]
            self.password = updated_config["PASSWORD_HASH"]

    def _show_warning_popup(self):
        """Exibe aviso ao usuário quando tentar aumentar o volume bloqueado."""
        if self.warning_open:
            return

        self.warning_open = True
        try:
            dialog = tk.Tk()
            dialog.title("AudioLocker - Áudio Bloqueado")
            dialog.geometry("360x165")
            dialog.resizable(False, False)
            dialog.attributes("-topmost", True)
            dialog.configure(bg="#2b2b2b")
            dialog.eval("tk::PlaceWindow . center")

            lbl_title = tk.Label(
                dialog,
                text="🔊 Volume Restrito",
                fg="#f0ad4e",
                bg="#2b2b2b",
                font=("Segoe UI", 12, "bold"),
            )
            lbl_title.pack(pady=(15, 5))

            lbl_msg = tk.Label(
                dialog,
                text="O volume deste computador está limitado ou bloqueado.\nPor favor, chame um atendente para desbloquear o áudio.",
                fg="white",
                bg="#2b2b2b",
                font=("Segoe UI", 9),
                justify="center",
            )
            lbl_msg.pack(pady=5, padx=15)

            def close_dialog():
                dialog.destroy()

            btn = tk.Button(
                dialog,
                text="Entendi",
                command=close_dialog,
                bg="#007acc",
                fg="white",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )
            btn.pack(pady=12, ipadx=18, ipady=2)

            dialog.bind("<Return>", lambda e: close_dialog())
            dialog.bind("<Escape>", lambda e: close_dialog())
            dialog.protocol("WM_DELETE_WINDOW", close_dialog)
            dialog.focus_force()

            dialog.mainloop()
        finally:
            self.warning_open = False

    def _show_password_window(self, action_type="unlock"):
        """Abre janela para validação de senha (Desbloquear, Configurações ou Sair)."""
        dialog = tk.Tk()
        dialog.title("AudioLocker")
        dialog.geometry("310x150")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.configure(bg="#2b2b2b")

        dialog.eval("tk::PlaceWindow . center")

        titles = {
            "unlock": "Senha para DESBLOQUEAR o Áudio:",
            "config": "Senha para abrir CONFIGURAÇÕES:",
            "exit": "Senha para SAIR do app:",
        }
        title_text = titles.get(action_type, "Digite a senha:")

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
            input_hash = hash_password(pwd)

            if input_hash == self.password or pwd == self.password:
                dialog.destroy()
                if action_type == "unlock":
                    self.unlock()
                elif action_type == "config":
                    self._open_edit_wizard()
                elif action_type == "exit":
                    self.running = False
                    self.tray_icon.stop()
            else:
                entry.delete(0, tk.END)
                messagebox.showerror(
                    "Erro", "Senha incorreta!", parent=dialog
                )

        btn_texts = {
            "unlock": "Desbloquear",
            "config": "Continuar",
            "exit": "Encerrar App",
        }
        btn_colors = {
            "unlock": "#007acc",
            "config": "#28a745",
            "exit": "#d9534f",
        }

        btn = tk.Button(
            dialog,
            text=btn_texts.get(action_type, "Confirmar"),
            command=validate,
            bg=btn_colors.get(action_type, "#007acc"),
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
                try:
                    was_reduced = self.audio.enforce_limit(self.max_volume)
                    if was_reduced and not self.warning_open:
                        threading.Thread(
                            target=self._show_warning_popup, daemon=True
                        ).start()
                except Exception:
                    pass

            time.sleep(self.check_interval)

    def run(self):
        audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        audio_thread.start()
        self.tray_icon.run()