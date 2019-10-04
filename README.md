# Nika :woman_technologist:
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

1. [Overview](#overview)
2. [My second title](#my-second-title)
## 1. Overview 
Some text.
## 2. Installation and Dependencies
Some text.
## 3. Modules
Some text.
### 3.1. colorprint
Some text.
### 3.2. config
Some text.
### 3.3. consumer
Some text.
### 3.4. error
Some text.
### 3.5. filter
Some text.
### 3.6. logger
Some text.
### 3.7. nika
Some text.
### 3.8. postgres
Some text.
### 3.9. producer
Some text.
### 3.10. util
Some text.

### Todos
 - Write Tests
 - Add FTP module
 - Add ClickHouse module

# 

## 1. Описание пакета
Пакет реализует подключение к источникам данных, логирование, аггрегирование, обработку ошибок и отправку результата получателю.

## 2. Для установки
`pip install Nika`

## 3. Для использования
- Cканируйте репозиторий
- В корне проекта создайте и заполните своими данными файл config.cfg следующего содержания:
```
[Nika]
name = {project name}
srcData = kafka
trgData = kafka

[kafkaConsumer]
topic = {topic}
groupID = {group}
brokers = {"ip:port", "ip:port", "ip:port"}

[kafkaProducer]
topic = {topic}
brokers = {"ip:port", "ip:port", "ip:port"}

[Logger]
level = debug
folder_to_log = Logs

[Postgres]
user = {user}
password = {pass}
host = {host}
port = {port}
database = {db_name}
```
- Затем с помощью `Docker` запустить минимум по 2 инстанса `Kafka` и `Zookeper`. 
Для этого запустите `docker-compose up`


## 4. Nika - Общая структура
- Nika
    - colorprint
    - config
    - consumer
    - error
    - filter
    - logger
    - nika
    - postgres
    - producer
    - response
    - util


## 5. Описание модулей и их компонентов
### 5.1 colorprint
Модуль Colorprint отвечает за отображение кода в цвете для нагладного эффекта

### 5.2 config
Данный модуль инициализирует и синхронизирует параметры конфигураций

### 5.3 consumer
Модуль реализует создание объекта подписчика (Consumer), который подключаяcь к Кафке, 
принимает и обрабатывает поступающие сообщения

### 5.4 error
Модуль, который осуществляет обработку возникшей ошибки для ее последующей записи в бд

### 5.5 filter

### 5.6 logger
Модуль для создания и ведения логов, которые записываются в корневую папку проекта.
В случае возникновения ошибок, производится их запись в бд.

### 5.7 nika
Основной модуль проекта Nika, собирающий все процессы воедино (подключение к бд, инициализация конфигов и логов, отправка и принятие сообщений).

### 5.8 postgres
Модуль для работы с базой данных (управление подключениями, заполнение базы данными)

### 5.9 producer
Данный модуль реализует создание объекта издателя (Producer), который подключается к Кафке и отправляет сообщения

### 5.10 response
Данный модуль формирует объект Response для его отправления в Кафку

### 5.11 util
Вспомогательные функции для проекта

## 6. Примеры использования
### 6.1 colorprint
### 6.1 config
### 6.1 consumer
### 6.1 error
### 6.1 filter
### 6.1 logger
### 6.1 nika
### 6.1 postgres
### 6.1 producer
### 6.1 response
### 6.1 util
