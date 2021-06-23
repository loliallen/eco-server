# Code refactoring

## Деплой
Имеется три апи:
1) eco_api - основное пользовательское апи. Используется на проде. 
   Поднимается на 5000 порту.
2) eco_api_stage - пользовательское апи. Используется для демонстрации
   нового функционала, который может сломать механизм работы со старым апи.
   Поднимается на 700 порту. 
3) eco_api_admin - админское апи. Используется на проде. Поднимается на
   8000 порту.

### Развернуть локально/на сервере
- Скачать себе образ eco_api (например  tag=0.1):
    ```bash
    docker pull intsynko1/eco_api:{tag}
    ```
  Аналогично для eco_api_stage, eco_api_admin

Для разработки локально можно использовать mongo из контейнера. На проде 
используется монго на облаке.
- Скачать себе образ mongo:
    ```bash
    docker pull mongo:latest
    ```

#### Запуск
- запуск mongo
  ```bash
  docker run -d -p 27017-27019:27017-27019 --name mongodb mongo
  ```
- запустить api
  ```bash
  docker run -d --name eco_api -p 5000:5000  intsynko1/eco_api:{tag} 
  ```
- чтобы контейнеры могли общаться:
  ```bash
  docker network create eco-net
  docker network connect eco-net mongodb
  docker network connect eco-net eco_api
  ```
  Так же можно было заранее создать сеть и при развертывании контейнера 
  прописать её в параметрах: `--net eco-net`
- посмотреть настройки сети
  ```bash
  docker network inspect eco-net
  ```
- проверить доступ с контейнера eco_api до mongodb
  ```bash
  docker exec -ti eco_api ping mongodb
  ```

### Обновление
- Собрать новый контейнер:
  ```bash
  docker build ./ -t eco_api
  ```
- Запушить собранный билд:
  ```bash
  docker tag eco_api:latest intsynko1/eco_api:{tag}
  docker push intsynko1/eco_api:{tag}
  ```
- Выполнить шаги "Развернуть локально/на сервере", "Запуск" на сервере


## SSL серитификат

- Создать сертификат:
```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
```

