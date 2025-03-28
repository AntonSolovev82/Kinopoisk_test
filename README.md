# Тестирование Кинопоиска
Автоматизировать UI- и API-тесты из финальной работы по ручному тестированию.
## Содержание

- [Описание](#описание)
- [Технологии](#технологии)
- [Структура](#структура)
- [Установка](#установка)
- [Запуск приложения](#запуск-приложения)
- [Запуск тестов](#запуск-тестов)
- [Ссылка на финальный проект](#Ссылка на финальный проект)
- [Рекомендации](#Рекомендации)

## Описание

Это веб-приложение позволяет пользователям:
- Авторизоваться и восстановить пароль.
- Искать фильмы по названию и актеру.
- Получать результаты поиска с возможностью фильтрации.

## Технологии

- Python
- Selenium
- pytest
- requests
- Allure для отчетности
## Структура
- config/ и data/:
настройки окружения (URL, пути до файлов и т. д.);
тестовые данные (логины, пароли, токены и т. д.).
- tests/: Директория, содержащая тестовые файлы.
test_api.py: Тесты, проверяющие функциональность API.
test_ui.py: Тесты, проверяющие функциональность пользовательского интерфейса.
## Установка

1. Клонируйте репозиторий:

## Запуск тестов

Для запуска тестов выполните следующие шаги:
1. Убедитесь, что все зависимости установлены. Если вы еще не сделали этого, выполните:
bash
   pip install -r requirements.txt
2. Для запуска тестов используйте команду:
bash
   pytest test/test_ui.py --alluredir=allureresults
   pytest test/test_api.py --alluredir=allureresults
3. Чтобы сгенерировать отчет Allure, выполните:
bash
   allure serve allure_results
## Ссылки на финальный проект
#### Вы можете ознакомиться с финальной версией проекта по  ссылкам:
- [Требования к проекту](https://qa-anton.yonote.ru/share/90b9aa18-e3ab-466c-9e2e-cfacc4ba295c)
- [Тест план](https://qa-anton.yonote.ru/share/95b396e2-ab9d-49d9-a361-c1268dc13e10)
- [Отчет о тестировании](https://qa-anton.yonote.ru/share/ad53fb26-23a3-4452-8ceb-c51957935473)

## Рекомендации:
### Некоторые причины, по которым в Selenium не рекомендуют использовать метод sleep:

1.Неопределённое поведение. Код с использованием sleep может работать не всегда, что приводит к ненадёжным тестам.  
2.Необходимое ожидание. Если установить статическое время ожидания, тесты могут ждать, даже если элемент уже загружен, что увеличивает время выполнения. 
3.Проблемы с параллельностью. В многопоточной среде внезапное использование sleep может заблокировать потоки, которые могут потребоваться для выполнения, что влияет на производительность. 
4.Отсутствие динамичности. Разные страницы могут загружаться с разной скоростью. Фиксированное время сна не учитывает varying время загрузки, что может привести к сбоям тестов. 
5.Сложность отладки. Когда тесты дают сбои из-за проблем с временем, может быть трудно определить, был ли сбой вызван сломанным тестом или неправильным временем ожидания. 
Вместо метода sleep рекомендуют использовать другие механизмы ожидания, такие как неявное или явное ожидание, которые делают взаимодействие элементов более предсказуемым

### Проблемы с капчей на кинопоиск
Возможно stealth может помочь в обходе капчи....
"""
from selenium_stealth import stealth
"""
