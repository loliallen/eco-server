
# 1. Filter
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
# 2. RecPoint
## [GET] /api/rec_points

| Query Params | Required | Description |
| ------------ | -------- | ----------- |
| id           | False | Get one recpoint |
| coords       | True | Send coords of map square |
| rec_type     | False | pass string |
| payback_type | False | pass string |
| filters      | False | array of var_names |

> Get with `coords` parameter

> `?coords=[[55, 55], ...]`
> - first left up point
> - second rigth up point
> - third rigth down point
> - fourth left down point

> `&rec_type=some_type`
> `&payback_type=some_type`
> `&filters=['some', 'filter']`

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

# 3. Marker

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


# 4. Auth

## [POST]/api/login
```json
{
    "username": "username",
    "password": "password"
}
```
## [POST]/api/users?code=code

`code` in parameter it's invitation code

`formdata`
```formdata
    name: string
    username: string
    password: string
```

> Create user
## [POST]/api/forget?username=username_email
### Start restoring proccess, you will recive an email with code

## [GET]/api/forget?username=username_email&code=code
### Validate a code

## [POST]/api/forget?username=username_email&code=104356&pwd=123
### Set new password


# 5. Invitations

## [POST]/api/invitation

### Create a new invitation
```json
{
    "user_id": "user_id"
}
```
`return`
```json
{
     "_id": {
        "$oid": "6038a09cc4736da49210b4f6"
    },
    "sender": {
        "$oid": "6037d762ae4bfe37c7c07c7a"
    },
    "code": 408927,
    "is_active": true,
    "ammount": 20
}
```



# 5. RecPoint offers

## [POST]/api/recoff
body
```json
{
    "coords": {
        "lat": 123.1,
        "lng": 123.1
    },
    "description": "srtr",
    "contact": {
        "name": "str",
        "phone": "phone"
    } 
}
```

# 6. Transactions

## [POST]/api/recycle

form-data:
| Key | Description |
| --- | ----------- |
| qrcode | string readed from qrcode |
| _to | recpoint id |
| filter_type | filter type |
| ammount | kgs |

response: 
```json
{
    "_from": {
        "_id": "603a47cf0c01a0a55af57c03",
        "code": 296362,
        "confirmed": false,
        "eco_coins": 0,
        "image": "",
        "name": "name",
        "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
        "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
        "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
        "username": "levaya.pochta.sobaka@gmail.com"
    },
    "_id": "6049a929102b529dc21e237b",
    "_to": {
        "_id": "602e0824e31d7249c7ffe450",
        "accept_types": [],
        "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
        "contacts": [
            {
                "name": "123",
                "phone": "(123) 123-1233"
            },
            {
                "name": "123123123",
                "phone": "(123) 123-1231"
            }
        ],
        "coords": {
            "lat": 55.739914,
            "lng": 49.2241303
        },
        "description": "123",
        "images": [],
        "name": "123",
        "partner": "602ddbe08b0e3817efe8f322",
        "payback_type": "paid",
        "reception_type": "recycle",
        "work_time": {
            "ВС": {
                "0": "10:25",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            },
            "ВТ": {
                "0": "10:25",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            },
            "ПН": {
                "0": "00:03",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            },
            "ПТ": {
                "0": "10:25",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            },
            "СБ": {
                "0": "10:25",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            },
            "СР": {
                "0": "10:25",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            },
            "ЧТ": {
                "0": "10:25",
                "1": "10:25",
                "2": "10:25",
                "3": "10:25"
            }
        }
    },
    "ammount": 123.0,
    "filter_type": {
        "_id": "602ef32013700f8cf099fcb3",
        "bad_words": [],
        "key_words": [],
        "name": "waasd",
        "var_name": "waasd"
    },
    "image": "",
    "reward": 0
}
```

## [GET] api/recycle?id=`<instance_id>`&type=`<instance_type>`

`<instance_id>` = ObjectId
`<instance_type>` = user|recpoint

response:
```json
[
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049a7aeb817338304764c40",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049a7c9b817338304764c42",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049a7d08654f8cd28f6b3be",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049a7e8d20893429c655c3c",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049a8144904106dd658a0f2",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049a929102b529dc21e237b",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "filter_type": {
            "_id": "602ef32013700f8cf099fcb3",
            "bad_words": [],
            "key_words": [],
            "name": "waasd",
            "var_name": "waasd"
        },
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049aa5757df2f8d01ca777d",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 123.0,
        "filter_type": {
            "_id": "602ef32013700f8cf099fcb3",
            "bad_words": [],
            "key_words": [],
            "name": "waasd",
            "var_name": "waasd"
        },
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049ac2b57df2f8d01ca777f",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 1233.0,
        "filter_type": {
            "_id": "602ef32013700f8cf099fcb3",
            "bad_words": [],
            "key_words": [],
            "name": "waasd",
            "var_name": "waasd"
        },
        "image": "",
        "reward": 0
    },
    {
        "_from": {
            "_id": "603a47cf0c01a0a55af57c03",
            "code": 296362,
            "confirmed": false,
            "eco_coins": 0,
            "image": "",
            "name": "name",
            "password": "sha256$G53StB0z$0f1194c73c10e6807260d83d44ed4fc66e046c1797170d3774edbb01a43fcbb7",
            "qrcode": "/static/users/f9d6e29c-78fe-11eb-ace7-f50348ab8d02.png",
            "token": "OLZRgFtmTJ2D2fyhqW4ZvU26SmxK0nkVIUKCs8VAU5Tn1CXYtiKuZy6FO2CpZQr1",
            "username": "levaya.pochta.sobaka@gmail.com"
        },
        "_id": "6049ac2f57df2f8d01ca7781",
        "_to": {
            "_id": "602e0824e31d7249c7ffe450",
            "accept_types": [],
            "address": "ул. Дубравная, 2д, Казань, Респ. Татарстан, Россия, 420139",
            "contacts": [
                {
                    "name": "123",
                    "phone": "(123) 123-1233"
                },
                {
                    "name": "123123123",
                    "phone": "(123) 123-1231"
                }
            ],
            "coords": {
                "lat": 55.739914,
                "lng": 49.2241303
            },
            "description": "123",
            "images": [],
            "name": "123",
            "partner": "602ddbe08b0e3817efe8f322",
            "payback_type": "paid",
            "reception_type": "recycle",
            "work_time": {
                "ВС": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ВТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПН": {
                    "0": "00:03",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ПТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СБ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "СР": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                },
                "ЧТ": {
                    "0": "10:25",
                    "1": "10:25",
                    "2": "10:25",
                    "3": "10:25"
                }
            }
        },
        "ammount": 1323.0,
        "filter_type": {
            "_id": "602ef32013700f8cf099fcb3",
            "bad_words": [],
            "key_words": [],
            "name": "waasd",
            "var_name": "waasd"
        },
        "image": "",
        "reward": 0
    }
]
```