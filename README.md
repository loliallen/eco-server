# EcoHub
Бэкэнд для приложения EcoHub. Используется база данных redis.

## Локальный запуск
Запуск апи пользователя:
```bash
python run.py user
```
Запуск апи админа:
```bash
python run.py admin
```

## Перевод
Сканировать все места, нуждающиеся в переводе:
```bash
pybabel extract -F src/translations/babel.cfg -k lazy_gettext -o src/translations/messages.pot src
```
Создать переводы:
```bash
pybabel update -i src/translations/messages.pot -d src/translations
```
Скомплировать перевод:
```bash
pybabel compile -f -d src/translations
```

## Деплой
Имеется три апи:
1) eco_api - основное пользовательское апи. Используется на проде. 
   Поднимается на 5000 порту.
2) eco_api_stage - пользовательское апи. Используется для демонстрации
   нового функционала, который может сломать обратную совместимость.
   Поднимается на 7000 порту. 
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

- запустить api
  ```bash
  docker run -d --name eco_api -p 5000:5000 -v ~/<путь до папки статики на сервере>/statics:/statics --env HOST='<host сервера>' --env STATIC_FOLDER='/statics'  intsynko1/eco_api:{tag} 
  ```


### Обновление
- Собрать новый контейнер:
  ```bash
  docker build -t eco_api -f <абсолютный путь до проекта>/deployment/api/prod/Docker ./
  ```
  После сборки проверьте работоспособность сборки через Запуск (предыдущий пункт)
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

