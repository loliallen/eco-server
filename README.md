## Models

### 1. Filter
## [GET] /api/filters
```json
{
  "_id": {
    "$oid": "123213213123"
  },
  "name": "Мукулатура",
  "var_name": "paper",
  "key_words": ["Газета", "Книга"],
  "bad_words": ["Газета", "Книга"],
}
```
### 2. RecPoint
## [GET] /api/rec_points

| Query Params | Required | Description |
| ------------ | -------- | ----------- |
| id           | False | Get one recpoint |
| coords       | True | Send coords of map square |

> Get with `coords` parameter

> `?coords=[[55, 55], ...]`
> - first left up point
> - second rigth up point
> - third rigth down point
> - fourth left down point

```json
{
  "_id": {
    "$oid": "1232132131123"
  },
  "name": "Название",
  "accept_types": [
    {
      "_id": {
        "$oid": "123213213123"
      },
      "name": "Мукулатура",
      "var_name": "paper",
      "key_words": ["Газета", "Книга"],
      "bad_words": ["Газета", "Книга"],
    }
  ],
  "coords": {
    "lat": 55,
    "lng": 55
  },
  "work_time": {
    "ПН": {
      "0": "9:00-13:00",
      "1": "15:00-18:00"
    }
  }
}
```
> Get one
```json
{
  "_id": {
    "$oid": "1232132131123"
  },
  "name": "Название",
  "images" : [
    "/static/rec_points/..."
  ],
  "address": "Казаньб что-то там",
  "description": "Описание",
  "accept_types": [
    {
      "_id": {
        "$oid": "123213213123"
      },
      "name": "Мукулатура",
      "var_name": "paper",
      "key_words": ["Газета", "Книга"],
      "bad_words": ["Газета", "Книга"],
    }
  ],
  "coords": {
    "lat": 55,
    "lng": 55
  },
  "work_time": {
    "ПН": {
      "0": "9:00-13:00",
      "1": "15:00-18:00"
    }
  }
}
```

## Routes

*ПП - Пункт Приема 
1. Поиск + Фильтры
2. Создание/Удаление/Обновление/Получение Фильтров
3. Создание/Удаление/Обновление/Получение ПП
---
- Газет => Газета
- Батар => Батарея, Батарейка 