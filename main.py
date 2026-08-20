from tray import AudioLockerTray

# Configurações Globais do AudioLocker
MAX_VOLUME = 0
CHECK_INTERVAL = 0.2
UNLOCK_TIME = 1800  # 30 minutos em segundos (use 10 para testes)
PASSWORD = "admin"

if __name__ == "__main__":
    app = AudioLockerTray(
        max_volume=MAX_VOLUME,
        check_interval=CHECK_INTERVAL,
        unlock_time=UNLOCK_TIME,
        password=PASSWORD,
    )
    app.run()