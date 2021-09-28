# EcoHub
Бэкэнд для приложения EcoHub. Используется база данных mongo.

## Локальный запуск
1) Развернуть mongo локально:
   ```bash
   docker run -d -p 27017-27019:27017-27019 --name mongo_db_local mongo
   ```
2) Запуск апи пользователя:
   ```bash  
   python run.py user
   ```
3) Запуск апи админа:
   ```bash
   python run.py admin
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

## Развернуть на сервере
Для развертывания понадобятся консольные команды docker и docker-compose.

1) Создать в папке deployment `.env` файл (скопировать `.env.exmaple`)
2) В корне проекта создать сертификаты
   ```bash
   openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
   ```
3) Собрать образ: 
   ```bash
   cd deployment
   [sudo] docker-compose build
   ```
4) Запутстить:
   ```bash
   [sudo] docker-compose up
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
