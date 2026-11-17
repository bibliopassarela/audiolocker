import hashlib
import json
import os
import sys
import tkinter as tk
from tkinter import messagebox


def get_config_path():
    """Retorna o caminho seguro do config.json na pasta %APPDATA%."""
    appdata_dir = os.path.join(os.getenv("APPDATA"), "AudioLocker")
    os.makedirs(appdata_dir, exist_ok=True)
    return os.path.join(appdata_dir, "config.json")


CONFIG_PATH = get_config_path()


def hash_password(password: str) -> str:
    """Gera um hash SHA-256 a partir da senha digitada."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_config():
    """Carrega as configurações do JSON se existir."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def save_config(max_volume, unlock_time, password_hash):
    """Salva as configurações no arquivo JSON usando o hash já processado."""
    data = {
        "MAX_VOLUME": max_volume,
        "UNLOCK_TIME": unlock_time,
        "PASSWORD_HASH": password_hash,
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run_setup_wizard():
    """Exibe a interface gráfica para a primeira configuração (Create)."""
    config_result = {}

    root = tk.Tk()
    root.title("AudioLocker - Configuração Inicial")
    root.geometry("380x360")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.configure(bg="#2b2b2b")
    root.eval("tk::PlaceWindow . center")

    lbl_title = tk.Label(
        root,
        text="Configuração Inicial do AudioLocker",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 12, "bold"),
    )
    lbl_title.pack(pady=(15, 10))

    frame = tk.Frame(root, bg="#2b2b2b")
    frame.pack(padx=20, fill="x")

    # 1. Campo de Senha (Obrigatório na criação)
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
    spin_vol.insert(0, "0")
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
        "3 horas": 10800,
        "4 horas": 14400,
    }

    selected_time = tk.StringVar(root)
    selected_time.set("1 hora (Padrão)")

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
        pwd_hash = hash_password(pwd)

        save_config(vol, time_in_seconds, pwd_hash)

        config_result["MAX_VOLUME"] = vol
        config_result["UNLOCK_TIME"] = time_in_seconds
        config_result["PASSWORD_HASH"] = pwd_hash

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


def run_edit_wizard(current_vol, current_time, current_pwd_hash):
    """Exibe janela dedicada para editar volume, tempo e/ou senha (Update)."""
    config_result = {}

    root = tk.Tk()
    root.title("AudioLocker - Editar Configurações")
    root.geometry("380x380")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.configure(bg="#2b2b2b")
    root.eval("tk::PlaceWindow . center")

    lbl_title = tk.Label(
        root,
        text="Editar Configurações",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 12, "bold"),
    )
    lbl_title.pack(pady=(15, 10))

    frame = tk.Frame(root, bg="#2b2b2b")
    frame.pack(padx=20, fill="x")

    # 1. Volume Máximo Permitido (Carrega o valor atual)
    lbl_vol = tk.Label(
        frame,
        text="Volume Máximo Bloqueado (%):",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_vol.pack(anchor="w", pady=(5, 2))
    spin_vol = tk.Spinbox(
        frame, from_=0, to=100, font=("Segoe UI", 10), justify="center"
    )
    spin_vol.delete(0, "end")
    spin_vol.insert(0, str(current_vol))
    spin_vol.pack(fill="x", pady=(0, 10))

    # 2. Tempo Limite de Desbloqueio (Carrega o tempo atual)
    lbl_time = tk.Label(
        frame,
        text="Tempo de Desbloqueio:",
        fg="white",
        bg="#2b2b2b",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_time.pack(anchor="w", pady=(5, 2))

    time_options = {
        "30 minutos": 1800,
        "1 hora (Padrão)": 3600,
        "2 horas": 7200,
        "3 horas": 10800,
        "4 horas": 14400,
    }

    # Identifica o texto correspondente aos segundos atuais
    default_label = "1 hora (Padrão)"
    for label, seconds in time_options.items():
        if seconds == current_time:
            default_label = label
            break

    selected_time = tk.StringVar(root)
    selected_time.set(default_label)

    opt_time = tk.OptionMenu(frame, selected_time, *time_options.keys())
    opt_time.config(font=("Segoe UI", 9), bg="#3c3c3c", fg="white", bd=0)
    opt_time["menu"].config(bg="#3c3c3c", fg="white")
    opt_time.pack(fill="x", pady=(0, 12))

    # 3. Nova Senha (Opcional na edição)
    lbl_pass = tk.Label(
        frame,
        text="Nova Senha (deixe em branco para manter a atual):",
        fg="#cccccc",
        bg="#2b2b2b",
        font=("Segoe UI", 9),
    )
    lbl_pass.pack(anchor="w", pady=(5, 2))
    entry_pass = tk.Entry(
        frame, show="•", font=("Segoe UI", 11), justify="center"
    )
    entry_pass.pack(fill="x", pady=(0, 15))

    def on_update():
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
        new_pwd = entry_pass.get().strip()

        # Se digitou uma nova senha, gera novo hash; caso contrário, mantém o atual
        if new_pwd:
            final_pwd_hash = hash_password(new_pwd)
        else:
            # Garante que se o valor atual era texto puro legado, converta para hash
            if len(current_pwd_hash) != 64:
                final_pwd_hash = hash_password(current_pwd_hash)
            else:
                final_pwd_hash = current_pwd_hash

        save_config(vol, time_in_seconds, final_pwd_hash)

        config_result["MAX_VOLUME"] = vol
        config_result["UNLOCK_TIME"] = time_in_seconds
        config_result["PASSWORD_HASH"] = final_pwd_hash

        messagebox.showinfo(
            "Sucesso",
            "Configurações atualizadas com sucesso!",
            parent=root,
        )
        root.destroy()

    btn_frame = tk.Frame(root, bg="#2b2b2b")
    btn_frame.pack(pady=5)

    btn_save = tk.Button(
        btn_frame,
        text="Salvar Alterações",
        command=on_update,
        bg="#007acc",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
    )
    btn_save.pack(side="left", padx=5, ipadx=10, ipady=3)

    btn_cancel = tk.Button(
        btn_frame,
        text="Cancelar",
        command=root.destroy,
        bg="#555555",
        fg="white",
        font=("Segoe UI", 10),
        relief="flat",
    )
    btn_cancel.pack(side="left", padx=5, ipadx=10, ipady=3)

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

    return config_result