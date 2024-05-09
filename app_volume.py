from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def set_volume(number: str):

    nums = {
        'один': 0.1,
        'два': 0.2,
        'три': 0.3,
        'четыре': 0.4,
        'пять': 0.5,
        'шесть': 0.6,
        'семь': 0.7,
        'восемь': 0.8,
        'девять': 0.9,
        'десять': 1.0
    }

    volume.SetMasterVolumeLevelScalar(nums[number], None)


def get_volume():
    current_volume = volume.GetMasterVolumeLevelScalar()
    return current_volume