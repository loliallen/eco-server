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
  "_id":{
    "$oid":"601d6a3843be561436285931"
  },
  "name":"name",
  "description":"Desc",
  "images":[
    "/static/recpoints/6fd962a8-67ca-11eb-a957-5ce0c558740a/0.png",
    "/static/recpoints/6fd962a8-67ca-11eb-a957-5ce0c558740a/1.png"
  ],
  "address":"Жиңү проспекты, 141, Казань, Респ. Татарстан, Россия, 420100",
  "reception_type":"utilisation",
  "payback_type":"free",
  "contacts":
  [
    {"phone":"(999) 999-9999","name":"Я крутой"},
    {"phone":"(999) 999-9999","name":"Такой молодец"}
  ],
  "coords":{
    "lat":55.77995109955695,
    "lng":49.21373411738282
  },
  "accept_types":[
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
  "work_time":{
    "ПН": ["12:03","12:03","12:03","12:03"],
    "ВТ": ["12:03","12:03","12:03","12:03"],
    "СР": ["12:03","12:03","12:03","12:03"],
    "ЧТ": ["12:03","12:03","12:03","12:03"],
    "ПТ": ["12:03","12:03","12:03","12:03"],
    "СБ": ["12:03","12:03","12:03","12:03"],
    "ВС": ["12:03","12:03","12:03","12:03"]
  }
}
```

### 3. Marker

## [GET]/api/markers/list/all
!!! warning
> Return array of markers `filter_vname` as `_id`, and filter names as `name` and marker description `description`

```json
[
  {
    "_id": "wasd",
    "items": [
      {"name": "wasd", "description": "wasd"}
    ]
  }
]
```

## Routes

*ПП - Пункт Приема 
1. Поиск + Фильтры
2. Создание/Удаление/Обновление/Получение Фильтров
3. Создание/Удаление/Обновление/Получение ПП
---
- Газет => Газета
- Батар => Батарея, Батарейка 