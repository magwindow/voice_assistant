"""Голосовой ассистент 'Меган'
Для получения справки, спроси у нее 'Что ты умеешь Меган?' или 'справка Меган'"""
import json
import queue
import vosk
import sounddevice as sd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import words
from skills import *
import voice

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


def recognize(data, vectorizer, clf):
    """Анализ распознанной речи"""

    # проверяем есть ли имя бота в data, если нет, то return
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # удаляем имя бота из текста
    data.replace(list(trg)[0], '')

    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    print('Меган:', answer)

    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    # озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name, ''))

    # запуск функции из skills
    exec(func_name + '()')


def main():
    """Обучаем матрицу ИИ и постоянно слушаем микрофон"""

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0], dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print('Вы говорите:', data)
                recognize(data, vectorizer, clf)
            # else:
            #     print(rec.PartialResult())


if __name__ == '__main__':
    main()
