В файле settings.py необходимо настроить почту для отправки сообщений:
"EMAIL_HOST_PASSWORD = 'код-пароль'" - в email можно создать пароль для автоматизации
"EMAIL_HOST_USER = 'почта для отправления'" - ваш email
В файле \Vending\Register\serializers.py - необходимо заменить 'rovda.roman@mail.ru' (он находится в функции create (send_mail ('rovda.roman@mail.ru')))

Краткий экскурс по архитектуре:
  1. Vending_api - Всё связанное с API и основной логикой.
     GET - api/vending-machines - отдаёт JSON С вендинговыми аппаратами
     GET - api/products - отдаёт JSON С продуктами
     GET - api/sales - отдаёт JSON С продажами. Общая цена продажи формируется по формуле 'цена продукта * кол-во'. Сразу добавляется в api/vending-machines/payout_amount
     GET - export/ - запрос на экспорт .csv файла
  3. Register - Всё связанное с регистрацией.
     GET - api/token/ - получение токена для логина
     GET - api/token/refresh/ - обновление токена для логина
     GET - register/ - запрос на регистрацию пользователя
     GET - confirm-email/ - подтверждение EMAIL
  4. media = сохраняет в себя .csv файл
  5. Базы данных Vending_api/models.py и Register/models.py
