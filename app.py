"""Голосовой ассистент 'Меган'
Для получения справки, спроси у нее 'Что ты умеешь Меган?' или 'справка Меган'"""
import json
import queue
import words
import vosk
import sounddevice as sd

q = queue.Queue()

# голосовую модель vosk нужно поместить в папку с файлами проекта
# https://alphacephei.com/vosk/
# https://alphacephei.com/vosk/models
model = vosk.Model('vosk_model_small')

# <--- по умолчанию
# или -> sd.default.device = 1, 3, python -m sounddevice просмотр
device = sd.default.device

# получаем частоту микрофона
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):
    """Добавляет в очередь семплы из потока.
    Вызывается каждый раз при наполнении blocksize в sd.RawInputStream"""
    q.put(bytes(indata))


# постоянная прослушка микрофона
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0], dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())['text']
            print('Вы говорите:', data)
        # else:
        #     print(rec.PartialResult())
