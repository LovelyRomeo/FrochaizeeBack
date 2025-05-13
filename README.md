В файле settings.py необходимо настроить почту для отправки сообщений:</br>
"EMAIL_HOST_PASSWORD = 'код-пароль'" - в email можно создать пароль для автоматизации</br>
"EMAIL_HOST_USER = 'почта для отправления'" - ваш email</br>
В файле \Vending\Register\serializers.py - необходимо заменить 'rovda.roman@mail.ru' (он находится в функции create (send_mail ('rovda.roman@mail.ru')))</br></br>

Краткий экскурс по архитектуре:</br>
  1. Vending_api - Всё связанное с API и основной логикой.</br>
     GET - api/vending-machines - отдаёт JSON С вендинговыми аппаратами</br>
     GET - api/products - отдаёт JSON С продуктами</br>
     GET - api/sales - отдаёт JSON С продажами. Общая цена продажи формируется по формуле 'цена продукта * кол-во'. Сразу добавляется в api/vending-machines/payout_amount</br>
     GET - export/ - запрос на экспорт .csv файла</br>
  3. Register - Всё связанное с регистрацией.</br>
     GET - api/token/ - получение токена для логина</br>
     GET - api/token/refresh/ - обновление токена для логина</br>
     GET - register/ - запрос на регистрацию пользователя</br>
     GET - confirm-email/ - подтверждение EMAIL</br>
  4. media = сохраняет в себя .csv файл</br>
  5. Базы данных Vending_api/models.py и Register/models.py</br>
