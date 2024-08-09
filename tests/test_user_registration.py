import pytest
import requests
import allure
from project_setup import TestSetup
from utils import generate_random_email, generate_random_password, generate_random_name

@pytest.mark.usefixtures("setup_teardown")
class TestUserRegistration:

    def setup_method(self):
        self.setup = TestSetup()

    @allure.title("Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание нового пользователя.")
    def test_create_unique_user(self):
        with allure.step("Регистрация нового пользователя"):
            response = self.setup.register_new_user()
            assert response.status_code == 200, f"Unexpected status code {response.status_code}. Response: {response.json()}"
            assert response.json()["success"] is True, "User registration was not successful"

    @allure.title("Создание существующего пользователя")
    @allure.description("Тест проверяет попытку создать пользователя с уже существующим email.")
    def test_create_existing_user(self):
        # Создание первого пользователя
        email = generate_random_email()
        password = generate_random_password()
        name = generate_random_name()

        with allure.step("Регистрация первого пользователя"):
            self.setup.register_new_user(email=email, password=password, name=name)

        with allure.step("Попытка создания пользователя с тем же email"):
            response = self.setup.register_new_user(email=email, password=password, name=name)
            assert response.status_code == 403, f"Unexpected status code {response.status_code}. Response: {response.json()}"
            assert response.json()["success"] is False, "User registration should have failed"
            assert response.json()["message"] == "User already exists", "Unexpected message for existing user"

    @allure.title("Создание пользователя с отсутствующим полем")
    @allure.description("Тест проверяет создание пользователя с отсутствующими обязательными полями.")
    def test_create_user_with_missing_field(self):
        incomplete_user = {
            "email": generate_random_email(),
            "password": generate_random_password()
            # Отсутствует имя
        }

        with allure.step("Попытка регистрации пользователя с отсутствующим полем"):
            response = requests.post(f"{self.setup.base_url}/auth/register", json=incomplete_user)
            assert response.status_code == 403, f"Unexpected status code {response.status_code}. Response: {response.json()}"
            assert response.json()["success"] is False, "User registration should have failed"
            assert response.json()["message"] == "Email, password and name are required fields", "Unexpected message for missing fields"









