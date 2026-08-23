from config_wizard import load_config, run_setup_wizard
from tray import AudioLockerTray

CHECK_INTERVAL = 0.2

if __name__ == "__main__":
    # Tenta carregar as configurações salvas
    config = load_config()

    # Se não houver configuração, executa o assistente inicial
    if not config:
        config = run_setup_wizard()

    # Inicia a aplicação na bandeja com as configurações validadas
    if config:
        app = AudioLockerTray(
            max_volume=config["MAX_VOLUME"],
            check_interval=CHECK_INTERVAL,
            unlock_time=config["UNLOCK_TIME"],
            password=config["PASSWORD"],
        )
        app.run()