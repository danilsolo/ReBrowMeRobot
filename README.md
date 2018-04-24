# Инструкция по установке

### 1. Установить python
Если убунта
~~~bash
sudo apt-get install python3
~~~

### 2. Установить необходимые библиотеки python
~~~bash
sudo pip3 install flask
sudo pip3 install pytelegrambotapi
~~~
### 3. Установить бота 
~~~bash
git clone https://github.com/danilsolo/ReBrowMeRobot
~~~
### 4. Установить сертификат в папку с ботом
##### 1. Установим пакет openssl
~~~bash
sudo apt-get install openssl
~~~
##### 2. Сгенерируем приватный ключ
~~~bash
openssl genrsa -out webhook_pkey.pem 2048
~~~
##### 3. Сгенерируем самоподписанный сертификат
~~~bash
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
~~~
> ВАЖНО!
> В Common Name обязательно указать айпи сервера

### 5. Запуск бота
~~~bash
nohup python3 bot.py &
~~~
