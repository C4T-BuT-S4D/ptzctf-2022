# OnegoCTF 2022

OnegoCTF — соревнование по защите информации от [Школы информационной безопасности ПетрГУ](https://vk.com/ptzctf). Задания разработаны командой [C4T BuT S4D](https://github.com/C4T-BuT-S4D/).

Проект поддержан Федеральным агентством по делам молодежи.


## Задания

| Название                                              | Сложность | Категория | Автор                                     |
|-------------------------------------------------------|-----------|-----------|-------------------------------------------|
| [rootsa](tasks/welcome/crypto-rootsa)                 | welcome   | crypto    | [keltecc](https://github.com/keltecc)     |
| [minecraft](tasks/welcome/joy_minecraft)              | welcome   | joy       | [jnovikov](https://github.com/jnovikov)   |
| [pycrev](tasks/welcome/pycrev)                   | welcome      | reverse       | [revervand](https://github.com/revervand)   |
| [eye-yes](tasks/easy/crypto-eye-yes)                       | easy      | crypto    | [keltecc](https://github.com/keltecc)     |
| [file](tasks/easy/for-file)         | easy   | forensics     | [revervand](https://github.com/revervand)   |
| [data-grinder](tasks/easy/ppc-data-grinder) | easy   | ppc  | [renbou](https://github.com/renbou) |
| [nginx](tasks/easy/web-nginx)                   | easy    | web       | [renbou](https://github.com/renbou)   |
| [StrangeAPI](tasks/medium/ppc-strange-api)                  | medium    | ppc    | [renbou](https://github.com/renbou)     |
| [m1check](tasks/medium/rev-m1check)                       | medium     | reverse     | [revervand](https://github.com/revervand)    |
| [site project](tasks/medium/web-adminsite)                 | medium     | web   | [jnovikov](https://github.com/jnovikov)     |
| [uptime](tasks/medium/web-uptime)                   | medium    | web       | [renbou](https://github.com/renbou)   |
| [strange-diffie-hellman](tasks/hard/crypto-strange-diffie-hellman)        | hard    | crypto    | [keltecc](https://github.com/keltecc) |
| [Kunteynir](tasks/hard/for-Kunteynir)                       | hard    | forensics     | [revervand](https://github.com/revervand)    |
| [pretty-notes](tasks/hard/prettynotes)                 | hard   | web   | [jnovikov](https://github.com/jnovikov)     |
| [SOS uslugi](tasks/hard/pwn-sos-uslugi)                       | hard    | pwn     | [revervand](https://github.com/revervand)    |

## Структура

1. Файл `README.md` содержит всю информацию о задании:

- описание, которое выдаётся участникам
- раздаточные материалы, которые выдаются участникам, если требуется
- разбор с описанием хода решения
- флаг к заданию

2. Директория `deploy` содержит необходимые настройки и файлы для запуска задания (если это сетевой сервис)

3. Директория `public` содержит файлы, которые необходимо выдать участникам
