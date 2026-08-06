import time

from audio import AudioController


class AudioLocker:

    MAX_VOLUME = 0
    CHECK_INTERVAL = 0.2

    def __init__(self):
        self.audio = AudioController()

        self.locked = True

    def lock(self):
        self.locked = True
        print("Sistema bloqueado.")

    def unlock(self):
        self.locked = False
        print("Sistema liberado.")

    def update(self):

        if not self.locked:
            return

        changed, current = self.audio.enforce_limit(self.MAX_VOLUME)

        if changed:
            print(
                f"Volume reduzido de {current}% para {self.MAX_VOLUME}%."
            )

    def run(self):

        print("AudioLocker iniciado.")

        while True:

            self.update()

            time.sleep(self.CHECK_INTERVAL)


if __name__ == "__main__":
    locker = AudioLocker()
    locker.run()