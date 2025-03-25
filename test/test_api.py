import allure
import requests
from config.settings import BASE_URL_API, API_TOKEN, YEAR, GENRE, ACTOR_EN

@allure.feature("Поиск фильмов")
@allure.story("Поиск фильма по названию")
@allure.title("Тест: Поиск фильма по названию 'Дюна'")
@allure.description("Проверяем, что API возвращает фильм с названием 'Дюна' и статус 200.")
def test_search_movie_by_title():
    title = "Дюна"
    response = requests.get(f"{BASE_URL_API}/movie/search?query={title}", headers=API_TOKEN)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

    response_title = response.json()["docs"][0]["name"]
    with allure.step("Проверка названия фильма в ответе"):
        assert response_title == title, f"Ожидалось название '{title}', но получено '{response_title}'"

@allure.story("Поиск фильма по жанру в определенный год")
@allure.title("Тест: Поиск фильмов по жанру и году")
@allure.description("Проверяем, что API возвращает фильмы определенного жанра за указанный год.")
def test_search_movie_by_genre():
    genre_to_search = GENRE
    response = requests.get(f"{BASE_URL_API}/movie?year={YEAR}&genres.name={genre_to_search}", headers=API_TOKEN)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200, f"Ошибка запроса: {response.status_code}"

    result_search = response.json()
    movies_list = result_search.get("docs", [])

    with allure.step("Проверка наличия фильмов в ответе"):
        assert movies_list, "Нет фильмов для заданных параметров"

    found_genre = False
    for movie in movies_list:
        genres = movie.get("genres", [])
        if any(genre["name"] == genre_to_search for genre in genres):
            found_genre = True
            break

    with allure.step("Проверка наличия жанра в результатах"):
        assert found_genre, f"Жанр '{genre_to_search}' не найден в результатах"

@allure.story("Поиск актера")
@allure.title(f"Тест: Поиск актера '{ACTOR_EN}'")
@allure.description(f"Проверяем, что API возвращает актера с именем '{ACTOR_EN}'.")
def test_search_actor():
    response = requests.get(f"{BASE_URL_API}/person/search?query={ACTOR_EN}", headers=API_TOKEN)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

    response_name = response.json()["docs"][0]["enName"]
    with allure.step("Проверка имени актера в ответе"):
        assert response_name == ACTOR_EN, f"Ожидалось имя '{ACTOR_EN}', но получено '{response_name}'"

@allure.story("Поиск с пустым запросом")
@allure.title("Тест: Поиск с пустым запросом")
@allure.description("Проверяем, что API возвращает статус 200 при пустом запросе на поиск фильмов.")
def test_search_with_empty_query():
    response = requests.get(f"{BASE_URL_API}/movie/search?", headers=API_TOKEN)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"


@allure.story("Поиск с другим методом (POST)")
@allure.title("Негативный тест: Поиск фильма с некорректными параметрами")
@allure.description("Проверяем, что API возвращает статус 404 при поиске фильма с использованием метода POST без необходимых параметров.")
def test_search_movie_post():
    # Выполняем POST-запрос
    response = requests.post(f"{BASE_URL_API}/movie/search?", headers=API_TOKEN)

    # Проверяем статус-код ответа
    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"

    # Дополнительно можно добавить информацию о теле ответа
    with allure.step("Проверка тела ответа"):
        allure.attach(response.text, "Ответ от API", allure.attachment_type.TEXT)




