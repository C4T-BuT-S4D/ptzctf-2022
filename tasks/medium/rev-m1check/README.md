# medium | reverse | m1check

## Описание
Казалось бы, обычный crackme.

Но что-то с ним явно не так, почему-то не запускается.

Да и формат какой-то странный!

## Информация
Бинарь под M1 с простым алгосом ксора.

## Решение
1. Находим LCG и разбираем генерацию случайных чисел
2. После генерации разбираемся с индексацией в массиве ключей
3. Пишем обратный алгоритм

[исходный код решения](solve/main.c)


## Флаг
`ptzctf{67423e253c9b4d8a0d2ac8a33bd58467}`