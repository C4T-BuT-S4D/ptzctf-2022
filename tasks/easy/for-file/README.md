# easy | forensics | file

## Описание
Нам тут какой-то странный файл попался.

Попробуй разобраться с ним, может получится что-то извлечь.

Тебе могу помочь знания формат файлов.

## Информация
Таск на работу с хекс-дампом и знание форматов файлов

## Решение

1. Преобразуем текстовый хексдамп в настоящий файл
2. Смотрим на заголовок и окончания и пониманем, что это перевёрнуться 7z архив
3. Разворачиваем дамп и получаем архив внутри которогое PNG
4. Открываем PNG и не видим флаг
5. Меняем границы высоты для PNG и получаем флаг

[скрипт решения](solve/solver.py)

## Флаг
`ptzctf{h3ll0_fr0m_xdd!}`