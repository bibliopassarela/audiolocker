from pycaw.pycaw import AudioUtilities


class AudioController:
    def __init__(self):
        self._endpoint = None
        self._get_volume_endpoint()

    def _get_volume_endpoint(self):
        """Tenta obter o controle de volume. Se não houver dispositivo, retorna None."""
        try:
            speakers = AudioUtilities.GetSpeakers()
            self._endpoint = speakers.EndpointVolume
            return self._endpoint
        except Exception:
            self._endpoint = None
            return None

    def enforce_limit(self, max_volume) -> bool:
        """
        Garante que o volume não ultrapasse o limite definido.
        Retorna True se o volume ultrapassou o limite e precisou ser reduzido.
        """
        if not self._endpoint:
            if not self._get_volume_endpoint():
                return False

        try:
            # Converte porcentagem para a escala do pycaw (0.0 a 1.0)
            target = max_volume / 100.0
            current_vol = self._endpoint.GetMasterVolumeLevelScalar()

            # Margem de 0.005 evita disparos falsos por arredondamento de ponto flutuante do Windows
            if current_vol > (target + 0.005):
                self._endpoint.SetMasterVolumeLevelScalar(target, None)
                return True

            return False
        except Exception:
            # Caso o dispositivo tenha sido desconectado/desabilitado durante o uso
            self._endpoint = None
            return False