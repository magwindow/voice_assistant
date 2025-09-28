import os
import sys
import webbrowser
import subprocess
import voice

import requests


def browser():
    """Открывает браузер заданный по умолчанию в системе с url указанным здесь"""
    webbrowser.open('https://www.google.com', new=2)


def game():
    """Нужно разместить путь к exe файлу любого вашего приложения"""
    try:
        subprocess.Popen(r'C:\Users\Антон\AppData\Local\Programs\GIMP 2\bin\gimp-2.10.exe')
    except:
        voice.speaker('Путь к файлу не найден, проверьте, правильный ли он')


def offpc():
    """Эта команда отключает ПК под управлением Windows"""
    os.system('shutdown \s')


def weather():
    """Для работы этого кода нужно зарегистрироваться на сайте
    https://openweathermap.org или переделать на ваше усмотрение под что-то другое"""
    try:
        params = {'q': 'London', 'units': 'metric', 'lang': 'ru', 'appid': 'ключ к API'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")
    except:
        voice.speaker('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def offBot():
    """Отключает бота"""
    sys.exit()


def passive():
    """Функция заглушка при простом диалоге с ботом"""
    pass
