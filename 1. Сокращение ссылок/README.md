## Идея
В современном мире очень часто используется система QR кодов, будь то авторизация пользователя или быстрый переход на какой-то сайт, так как телефон у нас всегда под рукой.

Хорошо было бы создавать помимо короткой ссылки так же QR код для перехода по короткой ссылке.

## Гипотеза:
1) Если использовать QR код, то это переход по ссылке осуществит большее количество человек.

## Трудозатраты
1) Необходимо создать новый столбец в базе данных для подсчета переходов на страницу с использованием QR кода.

2) Необходимо реализовать "ручку" которая бы принимала ```secret_key``` и возвращала бы нам Qr код для ссылки которой принадлежит ```secret_key``` или ошибку о том что ссылка с ```secret_key``` не найдена.

3) Обновить модель GetInfoAboutLinkResponse, чтобы отслеживать количество переходов по ссылке с использованием QR кода.

4) Обновить "ручку" ```api/v1/{short_code}```, добавив в нее отслеживание о том каким способом мы переходим по короткой ссылке и увеличивать соответствующий счетчик.

## MVP
Чтобы проверить прототип можно сверстать простенькую html с полями для создания короткой ссылки, сделать запрос на сервер, получить от него ответ в виде
```
short_url = "example.com/xyz" - короткая ссылка
secret_key - ключ для управления ссылкой
```
Затем клиентское приложение должно отправить запрос на нашу ручку по созданию QR кода и получить его в ответ.

В результате у клиента будет короткая ссылка, его секретный ключ, а так же QR код.

Время на реализацию минимального продукта уйдет ≈ 2 часа.

## Архитектура
Формальное описание интерфейса на OpenAPI 3.0 тут [openapi.yaml](openapi.yaml)

Добавление нового столбца ```number_of_use_qr_code``` в таблицу ```url_storage```

Добавление поля ```number_of_use_qr_code``` в модель ```GetInfoAboutLinkResponse```

Создание модели которая будет служить шаблоном ручки ```/api/v1/qr``` с методом ```POST```
```
QRRequest
  secret_key: UUID4
```
 Логика ```/api/v1/qr```:

Идем в базу, ищем запись где ```UrlStorage.secret_key = QRRequest.secret_key``` и ```UrlStorage.dt_expired >= current_time```.
  - Если такой записи отдаем пользователю ```HTTP_404_NOT_FOUND```.
  - Если такая запись существует.
    - Отдаем пользователю сгенерированный QR код в котором содержится url вида {host}:{port}{prefix}/{suffix}?id={UrlStorage.id} 
     

## АБ-тест
На ранних этапах функциональность с QR кодом можно показывать только пользователям desktop user agent.

Проследить с какого устройства чаще создавались короткие ссылки до и после внедрения фичи.

## Метрики
Основная метрика это количество переходов с использованием QR кода.

Ожидается что количество переходов с использованием QR будет превосходить количество обычных переходов.

## Демо
Видео: https://disk.yandex.ru/i/X0hC984cHS1hVA

Скрин пройденных тестов: https://disk.yandex.ru/i/ZOB7iyYEl8HvXg
