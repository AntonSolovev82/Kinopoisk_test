import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL, MOVIE_NAME, ACTOR, NO_MOVIE_NAME
from data.test_data import USER_CREDENTIALS
from selenium.common.exceptions import NoSuchElementException
"""
             Возможно stealth может помочь в обходе капчи....
from selenium_stealth import stealth
"""
"""
           Для отладки  кода используем sleep , но не используем метод в тестировании   
import time
"""



class Test_UI:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        with allure.step ("Заходим на сайт Кинопоиск"):
            self.driver = webdriver.Chrome()
            self.driver.get(f"{BASE_URL}")
            self.driver.implicitly_wait(30)
        with allure.step("Если появляется капча, пытаемся её нажать, иначе продолжаем следующие шаги."):
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".CheckboxCaptcha-Button").click()
            except NoSuchElementException:
                pass

        with allure.step("Если появляется реклама, сбрасываем, иначе продолжаем следующие шаги."):
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".styles_root__EjoL7").click()
            except NoSuchElementException:
                pass

        yield
        self.driver.quit()

    @allure.feature("Авторизация на сайте.")
    @allure.title("Тест авторизации пользователя.")
    @allure.description("Проверка успешной авторизации пользователя. Авторизуемся на сайте, используя входные данные.")
    @allure.id(1)
    @allure.severity("Blocker")
    def test_auth(self):
        with allure.step("Нажимаем кнопку 'Войти' на главной странице сайта."):
            self.driver.find_element(By.CSS_SELECTOR, ".styles_loginButton__LWZQp").click()
        with allure.step("Переключаемся на форму ввода логина почты"):
            try:
                # Ждем, пока элемент будет доступен и видим
                more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Ещё"))
                )
                more_button.click()

                # Ждем появления кнопки в выпадающем списке и кликаем по ней
                registration_buttons = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".RegistrationButtonPopup-itemButton"))
                )
                if len(registration_buttons) >= 3:
                    registration_buttons[2].click()  # Индекс 2 соответствует третьей кнопке
                else:
                    print("Третья кнопка не найдена.")

            except TimeoutException:
                assert False, "Не удалось найти или нажать кнопку 'Ещё' или кнопку регистрации"
        with allure.step("Заполняем поле логина."):
            self.driver.find_element(By.CSS_SELECTOR, "#passp-field-login").send_keys(USER_CREDENTIALS['username'])
            self.driver.find_element(By.CSS_SELECTOR, ".Button2-Text").click()
        with allure.step("Заполняем поле пароля."):
            password_input = self.driver.find_element(By.NAME, "passwd")
            password_input.send_keys(USER_CREDENTIALS['password'])
            password_input.send_keys(Keys.RETURN)

        with allure.step("Проверяем успешную авторизацию."):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_userName__XYZ"))  # Заменить на актуальный селектор
                )
                assert True  # Успешная авторизация
            except TimeoutException:
                assert False, "Авторизация не удалась"

    @allure.title("Тест восстановления пароля")
    @allure.description("Проверка процесса восстановления пароля")
    @allure.id(2)
    @allure.severity("Blocker")
    def test_password_recovery(self):
        with allure.step("Нажимаем кнопку 'Войти' на главной странице сайта."):
            self.driver.find_element(By.CSS_SELECTOR, ".styles_loginButton__LWZQp").click()
        with allure.step("Переключаемся на форму ввода логина почты"):
            try:
                # Ждем, пока элемент будет доступен и видим
                more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Ещё"))
                )
                more_button.click()

                # Ждем появления кнопки в выпадающем списке и кликаем по ней
                registration_buttons = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".RegistrationButtonPopup-itemButton"))
                )
                if len(registration_buttons) >= 3:
                    registration_buttons[2].click()  # Индекс 2 соответствует третьей кнопке
                else:
                    print("Третья кнопка не найдена.")

            except TimeoutException:
                assert False, "Не удалось найти или нажать кнопку 'Ещё' или кнопку регистрации"
        with allure.step("Заполняем поле логина."):
            login_input=self.driver.find_element(By.CSS_SELECTOR, "#passp-field-login")
            login_input.send_keys(USER_CREDENTIALS['username'])
            login_input.send_keys(Keys.RETURN)
        with allure.step("Нажимаем 'Не помню пароль'"):
            self.driver.find_element(By.CSS_SELECTOR, "a.Link.Link_pseudo.Link_view_default.Link_weight_medium").click()

        assert "Check your email" in self.driver.page_source  # Проверка сообщения об успешной отправке

    @allure.title("Тест поиска фильма по названию")
    @allure.description("Проверка поиска фильма по его названию")
    @allure.id(3)
    @allure.severity("Blocker")
    def test_search_movie_by_title(self):
        search_bar = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys(f"{MOVIE_NAME}")
        search_bar.send_keys(Keys.ENTER)

        movie_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, f"{MOVIE_NAME}"))
        )
        movie_link.click()

        assert f"{MOVIE_NAME}" in self.driver.title, f"Не удалось открыть страницу фильма '{MOVIE_NAME}'"

    @allure.title("Тест поиска по актеру")
    @allure.description("Проверка поиска фильмов по имени актера")
    @allure.id(4)
    @allure.severity("Blocker")
    def test_search_movie_by_actor(self):
        search_bar = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys(f"{ACTOR}")
        search_bar.send_keys(Keys.ENTER)

        actor_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, f"{ACTOR}"))
        )
        actor_link.click()

        assert f"{ACTOR}" in self.driver.title, f"Не удалось открыть страницу актера  '{ACTOR}'"

    @allure.title("Тест поиска по несуществующему названию")
    @allure.description("Проверка поведения системы при поиске по несуществующему названию фильма")
    @allure.id(5)
    @allure.severity("Blocker")
    def test_search_non_existent_movie(self):
        search_bar = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys(f"{NO_MOVIE_NAME}")
        search_bar.send_keys(Keys.ENTER)
        with (allure.step("Поиск в ответе нужного результата")):
            try :
                no_movie_name =self.driver.find_elements("//*[contains(., 'К сожалению, по вашему запросу ничего не найдено...')]") ###?????
                assert len(no_movie_name)>0
            except TimeoutException:
                assert False,"Ошибка поиска "