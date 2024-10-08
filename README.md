## Трекер полезных привычек (DRF)

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Заказчик прочитал книгу, впечатлился и обратился к вам с запросом реализовать трекер полезных привычек.

В книге хороший пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

**я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]**

За каждую полезную привычку необходимо себя вознаграждать или сразу после делать приятную привычку. Но при этом привычка не должна расходовать на выполнение больше двух минут.

Полезная привычка — это само действие, которое пользователь будет совершать и получать за его выполнение определенное вознаграждение (приятная привычка или любое другое вознаграждение).

Приятная привычка — это способ вознаградить себя за выполнение полезной привычки. Приятная привычка указывается в качестве связанной для полезной привычки (в поле «Связанная привычка»).

Для полноценной работы сервиса необходимо реализовать работу с отложенными задачами для напоминания о том, в какое время какие привычки необходимо выполнять.
Требуется интегрировать сервис с мессенджером Телеграм, который будет заниматься рассылкой уведомлений.

#### Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными .env.example.
+ ``python manage.py createusers`` - создать пользователей
+ ``python manage.py seed`` - сидирование таблиц
+ ``python manage.py collectstatic`` - сборка статических файлов
+ JWT - авторизация
+ Запуск отложенных задач: ``celery -A config worker -l INFO``
+ Запуск периодических задач: ``celery -A config worker --beat --scheduler django --loglevel=info``
+ Тест: ``coverage run --source='.' manage.py test && coverage html``
+ Flake8 (результаты теста - папка htmlcov): ``flake8``
+ Сборка docker-контейнера
```
  docker network create atomichabitnet
  docker-compose up --build - пересобрать контейнеры
  docker-compose up - запуск контейнеров
```

#### Документация
+ http://127.0.0.1:8000/redoc/
+ http://127.0.0.1:8000/swagger/

#### Модели
+ authen_drf
    * ``User`` - пользователь: почта, id телеграм чата, телефон, аватар, токен
+ habit
    * ``Periodicity`` - периодичность: название, интервал
    * ``Location``- место: название
    * ``Action`` - действие: название, признак приятного действия
    * ``Reward``- вознаграждение: название
    * ``Habit``- привычка: автор, место, действие, время, периодичность, время выполнения, общедоступность
    * ``PleasantHabit`` - приятная привычка-вознаграждение: пользователь, привычка
    * ``UsefulHabit`` - полезная привычка: пользователь, привычка, вознаграждение, приятная привычка
  
#### Валидация (расположена в моделях)
* ``UsefulHabit.clean()``
  + исключён одновременный выбор связанной привычки и указания вознаграждения 
  + в качестве действия можно выбрать только полезное действие
  + возможность использование указанную привычку
* ``Habit.clean()``
  + Время выполнения не должно превышать 120 секунд
* В качестве связанной привычки может быть указана только приятная привычка ``PleasantHabit``
* ``Periodicity.clean()`` - периодичность не может быть больше 7 дней

#### Пагинация:
``HabitViewSet``, ``PleasantHabitViewSet``, ``UsefulHabitViewSet``

#### Права доступа
+ ``IsAuthorPermission`` - проверка создателя объекта
+ ``IsOwnerPermission`` - проверка создателя объекта
+ ``IsSuperUserPermission`` - проверка суперпользователя

#### Эндпоинты
+ Пользователь (*user/*): регистрация, авторизация, CRUD
+ Периодичность (*periodicity/*): список, добавление, удаление
+ Местоположение (*location/*): список, добавление, удаление
+ Действие (*action/*): список, добавление, удаление
+ Вознаграждение (*reward/*): список, добавление, удаление
+ Список публичных привычек (*public-habit/*)
+ Привычка (*habit/*): CRUD
+ Полезная привычка (*useful-habit/*): CRUD
+ Приятная привычка (*pleasant-habit/*): CRUD
+ Документация (*/redoc, /swagger*) 

#### Интеграция с телеграмом
+ ``check_habit_time()`` - каждый час проверяет привычки, которые нужно выполнить в ближайший час и рассылает уведомления в телеграм каналы
+ ``habit.tasks.send_message()`` - Отправляет отложенно сообщение в телеграм чат

#### CORS
Настроен на http://127.0.0.1:8000


