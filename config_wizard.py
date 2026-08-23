import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Garante que o config.json seja salvo na mesma pasta do executável
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def load_config():
    """Carrega as configurações do JSON se existir."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def save_config(max_volume, unlock_time, password):
    """Salva as configurações no arquivo JSON."""
    data = {
        "MAX_VOLUME": max_volume,
        "UNLOCK_TIME": unlock_time,
        "PASSWORD": password,
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run_setup_wizard():
    """Exibe a interface gráfica para primeira configuração."""
    config_result = {}

    root = tk.Tk()
    root.title("AudioLocker - Configuração Inicial")
    root.geometry("380x360")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.configure(bg="#2b2b2b")
    root.eval("tk::PlaceWindow . center")

    # Título
    lbl_title = tk.Label(
        root,
        text="Configuração do AudioLocker",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 12, "bold"),
    )
    lbl_title.pack(pady=(15, 10))

    frame = tk.Frame(root, bg="#2b2b2b")
    frame.pack(padx=20, fill="x")

    # 1. Campo de Senha (Obrigatório)
    lbl_pass = tk.Label(
        frame,
        text="Senha de Administrador (Obrigatório):",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_pass.pack(anchor="w", pady=(5, 2))
    entry_pass = tk.Entry(
        frame, show="•", font=("Segoe UI", 11), justify="center"
    )
    entry_pass.pack(fill="x", pady=(0, 10))

    # 2. Volume Máximo Permitido
    lbl_vol = tk.Label(
        frame,
        text="Volume Máximo Bloqueado (%):",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 9),
    )
    lbl_vol.pack(anchor="w", pady=(5, 2))
    spin_vol = tk.Spinbox(
        frame, from_=0, to=100, font=("Segoe UI", 10), justify="center"
    )
    spin_vol.delete(0, "end")
    spin_vol.insert(0, "0")  # Padrão: 0%
    spin_vol.pack(fill="x", pady=(0, 10))

    # 3. Tempo Limite de Desbloqueio
    lbl_time = tk.Label(
        frame,
        text="Tempo de Desbloqueio:",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 9),
    )
    lbl_time.pack(anchor="w", pady=(5, 2))

    time_options = {
        "30 minutos": 1800,
        "1 hora (Padrão)": 3600,
        "2 horas": 7200,
        "4 horas": 14400,
    }

    selected_time = tk.StringVar(root)
    selected_time.set("1 hora (Padrão)")  # Padrão: 1h

    opt_time = tk.OptionMenu(frame, selected_time, *time_options.keys())
    opt_time.config(font=("Segoe UI", 9), bg="#3c3c3c", fg="white", bd=0)
    opt_time["menu"].config(bg="#3c3c3c", fg="white")
    opt_time.pack(fill="x", pady=(0, 15))

    def on_save():
        pwd = entry_pass.get().strip()
        if not pwd:
            messagebox.showerror(
                "Atenção", "A senha é obrigatória!", parent=root
            )
            return

        try:
            vol = int(spin_vol.get())
            if not (0 <= vol <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Volume inválido! Digite um número de 0 a 100.",
                parent=root,
            )
            return

        time_in_seconds = time_options[selected_time.get()]

        save_config(vol, time_in_seconds, pwd)

        config_result["MAX_VOLUME"] = vol
        config_result["UNLOCK_TIME"] = time_in_seconds
        config_result["PASSWORD"] = pwd

        messagebox.showinfo(
            "Sucesso",
            "Configurações salvas! O AudioLocker será iniciado.",
            parent=root,
        )
        root.destroy()

    btn_save = tk.Button(
        root,
        text="Salvar e Iniciar",
        command=on_save,
        bg="#28a745",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
    )
    btn_save.pack(pady=10, ipadx=10, ipady=3)

    # Impede fechar a janela sem configurar
    def on_close():
        if messagebox.askyesno(
            "Sair",
            "O app não pode iniciar sem a senha. Deseja encerrar?",
            parent=root,
        ):
            root.destroy()
            sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    return config_result