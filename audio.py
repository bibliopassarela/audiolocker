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

    def enforce_limit(self, max_volume):
        """Garante que o volume não ultrapasse o limite definido."""
        # Se não tínhamos um endpoint válido, tenta buscar novamente
        if not self._endpoint:
            if not self._get_volume_endpoint():
                return  # Nenhum áudio conectado no momento, ignora a execução

        try:
            # Converte porcentagem para a escala do pycaw (0.0 a 1.0)
            target = max_volume / 100.0
            current_vol = self._endpoint.GetMasterVolumeLevelScalar()

            if current_vol > target:
                self._endpoint.SetMasterVolumeLevelScalar(target, None)
        except Exception:
            # Caso o dispositivo tenha sido desconectado/desabilitado durante o uso
            self._endpoint = None