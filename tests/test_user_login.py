import pytest
import allure
from project_setup import TestSetup
from utils import generate_random_email, generate_random_password

@pytest.mark.usefixtures("setup_teardown")
class TestUserLogin:

    def setup_method(self):
        self.setup = TestSetup()

    @allure.title("Логин под существующим пользователем")
    @allure.description("Тест проверяет успешный логин под существующим пользователем с правильными учетными данными.")
    def test_login_existing_user(self):
        with allure.step("Регистрация нового пользователя"):
            response = self.setup.register_new_user()
            assert response.status_code == 200
            assert response.json().get("success") is True

        with allure.step("Логин под существующим пользователем"):
            response = self.setup.login_user(self.setup.created_user['email'], self.setup.created_user['password'])
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title("Логин с неправильными учетными данными")
    @allure.description("Тест проверяет попытку логина с неправильными учетными данными. Ожидается ошибка 401.")
    @pytest.mark.parametrize("email, password", [
        (generate_random_email(), generate_random_password()),
        (generate_random_email(), generate_random_password())
    ])
    def test_login_incorrect_credentials(self, email, password):
        with allure.step(f"Попытка логина с email={email} и password={password}"):
            response = self.setup.login_user(email, password)
            assert response.status_code == 401
            assert response.json().get("message") == "email or password are incorrect"
