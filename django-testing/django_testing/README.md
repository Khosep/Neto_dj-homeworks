Тестирование Django-приложения
====

## Описание

Есть бекенд простого приложения с курсами и списком студентов. Вся логика для бекенда уже есть в заготовке, но совершенно нет тестов.

## Что нужно сделать

Вам необходимо написать тесты для текущей логики приложения.

Заведите фикстуры:
- для api-client'а
- для фабрики курсов
- для фабрики студентов

В качестве библиотеки для фабрик используйте `model_bakery` (https://github.com/model-bakers/model_bakery).

Добавьте следующие тест-кейсы:

- проверка получения 1го курса (retrieve-логика)
  - создаем курс через фабрику
  - строим урл и делаем запрос через тестовый клиент
  - проверяем, что вернулся именно тот курс, который запрашивали
- проверка получения списка курсов (list-логика)
  - аналогично – сначала вызываем фабрики, затем делаем запрос и проверяем результат
- проверка фильтрации списка курсов по `id`
  - создаем курсы через фабрику, передать id одного курса в фильтр, проверить результат запроса с фильтром
- проверка фильтрации списка курсов по `name`
- тест успешного создания курса
  - здесь фабрика не нужна, готовим JSON-данные и создаем курс
- тест успешного обновления курса
  - сначала через фабрику создаем, потом обновляем JSON-данными
- тест успешного удаления курса


Все тесты должны явно проверять код возврата.

Не забывайте использовать декоратор `@pytest.mark.django_db`, чтобы тесты использовали базу.

Запуск тестов делается через команду:
```
$ pytest
```

Перед началом работы убедитесь, что все зависимости установлены (dev-зависимости указаны в `requirements-dev.txt`) и тесты успешно запускаются. Вы должны увидеть:

```
$ pytest
======== test session starts =====

...
collected 1 item

tests/students/test_courses_api.py F                                                                                                                                          [100%]

====== FAILURES ====
_____ test_example ____

    def test_example():
>       assert False, "Just test example"
E       AssertionError: Just test example
E       assert False

tests/students/test_courses_api.py:2: AssertionError
=== short test summary info ===
FAILED tests/students/test_courses_api.py::test_example - AssertionError: Just test example
===== 1 failed in 0.21s =====
```

Этот тест можете удалить и написать в этом файле свои тесты.

## Документация

pytest: https://docs.pytest.org/en/stable/ 

pytest-django: https://pytest-django.readthedocs.io/en/latest/ 

тестирование DRF: https://www.django-rest-framework.org/api-guide/testing/

## Дополнительные задания (необязательные для выполнения)

### Ограничить число студентов на курсе

Добавьте валидацию на максимальное число студентов на курсе – 20. Подумайте, как протестировать это ограничение, не создавая 20 сущностей в базе данных.

__Подсказка:__ задайте максимальное число студентов в `settings.py`: `MAX_STUDENTS_PER_COURSE`. В тестах используйте `parametrize` и фикстуру `settings` (https://pytest-django.readthedocs.io/en/latest/helpers.html#settings), чтобы переопределить параметр.

Протестируйте как неудачный исход, так и успешный.

## Документация по проекту

Для запуска проекта необходимо:

Установить зависимости:

```bash
pip install -r requirements-dev.txt
```

Вам необходимо будет создать базу в postgres и прогнать миграции:

```base
manage.py migrate
```

Выполнить команду:

```bash
pytest
```