# Лекционное задание #1

Лекционное задание на эксперименты с возведением в степень матриц смежности графов

## Запуск построения тестового графа (Петерсена)

Клонируйте репозиторий (скачайте все файлы из репозитория, если git не установлен

`git clone git@github.com:kazumasatovich/Lecture_assignment_Pozdnyakov_LETI.git`

Перейдите в папку проекта

`cd Lecture_assignment_Pozdnyakov_LETI`

Создайте виртуальное окружение

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -e .`

Установка зависимостей:

`pip install -r requirements.txt`

Из корня проекта ~/src/matrix_graph

`python3 demo.py`

## Запуск эксперимента со скоростью работы возведения в степень и проверки корректности алгоритма на графе Петерсена

Клонируйте репозиторий (скачайте все файлы из репозитория, если git не установлен

`git clone git@github.com:kazumasatovich/Lecture_assignment_Pozdnyakov_LETI.git`

Перейдите в папку проекта

`cd Lecture_assignment_Pozdnyakov_LETI`

Создайте виртуальное окружение

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -e .`


Установка зависимостей:

`pip install -r requirements.txt`

Установите новый сид в `experiments.py` или оставьте стандартный (174)

Из корня проекта ~/src/matrix_graph

`python3 experiment.py`

Граф и график замеров сохранится в `figures/`

<3
