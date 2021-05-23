# Code refactoring


## Деплой

### Развернуть локально/на сервере
- Скачать себе образ eco_api (например  tag=0.1):
    ```bash
    docker pull intsynko1/eco_api:{tag}
    ```

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
  docker run -d --name eco_api -p 5000:5000 --env DB_URL=mongodb intsynko1/eco_api:{tag} 
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

