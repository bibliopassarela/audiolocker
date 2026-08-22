import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class AudioController:

    def __init__(self):
        self.volume_interface = None

    def _get_interface(self):
        """Busca o dispositivo de som ativo. Se não houver (fone desplugado ou áudio desativado),

        retorna None sem derrubar o programa.
        """
        if self.volume_interface:
            return self.volume_interface

        try:
            # Inicializa a COM thread necessária para rodar em segundo plano
            comtypes.CoInitialize()

            speakers = AudioUtilities.GetSpeakers()
            if speakers:
                # Conecta com a API nativa do Windows (Core Audio)
                interface = speakers.Activate(
                    IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None
                )
                self.volume_interface = interface.QueryInterface(
                    IAudioEndpointVolume
                )
                return self.volume_interface
        except Exception:
            # Dispositivo indisponível, desativado no Windows ou fone desconectado
            self.volume_interface = None

        return None

    def get_volume(self):
        """Retorna o volume mestre atual (0 a 100). Se falhar, assume 0."""
        interface = self._get_interface()
        if not interface:
            return 0

        try:
            # GetMasterVolumeLevelScalar retorna um decimal de 0.0 a 1.0
            return round(interface.GetMasterVolumeLevelScalar() * 100)
        except Exception:
            # Se o fone for desplugado no meio da leitura, limpa a interface para reconectar depois
            self.volume_interface = None
            return 0

    def set_volume(self, level_percentage):
        """Aplica o volume desejado em porcentagem."""
        interface = self._get_interface()
        if not interface:
            return False

        try:
            scalar_level = max(0.0, min(1.0, level_percentage / 100.0))
            interface.SetMasterVolumeLevelScalar(scalar_level, None)
            return True
        except Exception:
            self.volume_interface = None
            return False

    def enforce_limit(self, max_volume):
        """Se o volume do Windows estiver acima do limite, reduz imediatamente."""
        current = self.get_volume()
        if current > max_volume:
            if self.set_volume(max_volume):
                return True, current
        return False, current