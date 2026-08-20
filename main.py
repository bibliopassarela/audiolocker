import getpass
import threading
import time
from audio import AudioController


class AudioLocker:
    MAX_VOLUME = 0
    CHECK_INTERVAL = 0.2
    UNLOCK_TIME = 10  # Tempo em segundos para testes (ex: 1800 para 30 min)
    PASSWORD = "admin"  # Senha padrão

    def __init__(self):
        self.audio = AudioController()
        self.locked = True
        self.unlocked_until = 0

    def lock(self):
        self.locked = True
        print("\n[Status] Sistema BLOQUEADO.")

    def unlock(self):
        self.locked = False
        self.unlocked_until = time.time() + self.UNLOCK_TIME
        print(f"\n[Status] Sistema LIBERADO por {self.UNLOCK_TIME} segundos.")

    def update(self):
        # Verifica se o tempo de liberação expirou
        if not self.locked:
            if time.time() >= self.unlocked_until:
                print("\n[Alerta] Tempo de liberação expirou!")
                self.lock()
            return

        # Aplica o limite se estiver bloqueado
        changed, current = self.audio.enforce_limit(self.MAX_VOLUME)
        if changed:
            print(
                f"\n[AudioLocker] Volume reduzido de {current}% para {self.MAX_VOLUME}%."
            )

    def monitor_loop(self):
        """Loop contínuo rodando em background (Thread secundária)."""
        while True:
            self.update()
            time.sleep(self.CHECK_INTERVAL)

    def auth_loop(self):
        """Loop de interface CLI rodando na Thread principal."""
        print("=== AudioLocker Iniciado ===")
        print("Digite a senha e pressione Enter para desbloquear.")

        while True:
            if self.locked:
                # getpass oculta a senha digitada no terminal
                pwd = getpass.getpass("Digite a senha: ")
                if pwd == self.PASSWORD:
                    self.unlock()
                else:
                    print("Senha incorreta!")
            else:
                # Enquanto estiver desbloqueado, aguarda a expiração
                time.sleep(1)

    def run(self):
        # Inicia o monitor de áudio em uma thread daemon
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()

        # Roda a interface de senha na thread principal
        self.auth_loop()


if __name__ == "__main__":
    locker = AudioLocker()
    locker.run()