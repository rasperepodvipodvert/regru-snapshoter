# regru-snapshoter

Позволяет автоматически управлять снимками виртулаьных машин в REG.RU, использовать снепшоты как бэкапы

## Настройка

### Конфиг

Для использования необходимо передать в енвароменте следующие параметры:

`API_KEY` - [Ключик для доступа к API](https://developers.cloudvps.reg.ru/getting-started/authentication.html)\
`TIME_DELTA` - число, обозначающее дни, сколько хранить снепшот

либо поместить их в `.env` рядом со скриптом

```
API_KEY = 119a29d408f043c93437a1c374f58819364837a709571cd322f3bae89e2e6773c85676bd8cb5a5459898a29c42c22d50
TIME_DELTA = 7
```

### Список VM которые бэкапить

Список VM лежит в файлике `vm_list.txt`

## Ссылки:

- [Снепшоты](https://developers.cloudvps.reg.ru/snapshots/index.html)
- [Виртуальные серверы](https://developers.cloudvps.reg.ru/reglets/index.html)