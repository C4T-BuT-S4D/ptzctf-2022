# PTZCTF 2022 | Easy / Crypto | eye-yes

## Описание

> Мне рассказали, что режим CBC гораздо безопаснее, чем ECB. Теперь я использую его всегда.
> 
> `nc BEBRABEBRA 17171`

## Раздатка

Участникам нужно выдать файлы:

* [public/crypto-eye-yes.zip](public/crypto-eye-yes.zip)

## Деплой

```
docker-compose up --build -d
```

## Решение

В таске используется шифр AES в режиме CBC. Уязвимость в том, что IV равен ключу шифрования. Мы можем достать ключ, если вспомним как работает CBC и применим следующую атаку:

1. Шифруем два нулевых блока, тогда:

```
block1 = E(IV ^ 0) = E(IV) = E(key)
block2 = E(block1 ^ 0) = E(block1) = E(E(key))
```

2. Расшифровываем `block2`, тогда:

```
block3 = IV ^ D(block2) = IV ^ D(E(E(key))) = IV ^ E(key) = key ^ E(key)
```

3. Ксорим `block1` и `block3`:

```
block1 ^ block3 = E(key) ^ key ^ E(key) = key
```

Получаем ключ, который является флагом. Осталось обернуть в `ptzctf{}`.

**Пример решения**: [solution/solver.py](solution/solver.py)

## Флаг

```
ptzctf{AES_k3y_rec0very}
```
