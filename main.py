from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

# Volume máximo permitido (0 a 100)
MAX_VOLUME = 0


# ==========================================================
# ÁUDIO
# ==========================================================

def get_audio_controller():
    device = AudioUtilities.GetSpeakers()

    interface = device.EndpointVolume

    return interface


def get_current_volume():
    volume = get_audio_controller()
    return round(volume.GetMasterVolumeLevelScalar() * 100)


def set_volume(percent):
    percent = max(0, min(100, percent))

    volume = get_audio_controller()
    volume.SetMasterVolumeLevelScalar(percent / 100, None)


def enforce_limit():
    current = get_current_volume()

    if current > MAX_VOLUME:
        set_volume(MAX_VOLUME)
        print(
            f"Volume reduzido de {current}% para {MAX_VOLUME}%."
        )
    else:
        print(
            f"Volume atual ({current}%) está dentro do limite."
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    enforce_limit()