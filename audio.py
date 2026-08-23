from pycaw.pycaw import AudioUtilities


class AudioController:
    """Responsável por controlar o áudio do Windows."""

    def __init__(self):
        self._endpoint = AudioUtilities.GetSpeakers().EndpointVolume

    def get_volume(self):
        """Retorna o volume atual em porcentagem."""
        return round(self._endpoint.GetMasterVolumeLevelScalar() * 100)

    def set_volume(self, percent):
        """Define o volume em porcentagem."""
        percent = max(0, min(100, percent))
        self._endpoint.SetMasterVolumeLevelScalar(percent / 100, None)

    def enforce_limit(self, limit):
        """Garante que o volume não ultrapasse o limite."""
        current = self.get_volume()

        if current > limit:
            self.set_volume(limit)
            return True, current

        return False, current