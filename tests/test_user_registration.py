import pytest
import requests
import allure
from project_setup import TestSetup
from utils import generate_random_email, generate_random_password, generate_random_name
from messages import (
    USER_ALREADY_EXISTS,
    REGISTRATION_FAILED,
    UNEXPECTED_STATUS_CODE,
    MISSING_FIELDS_MESSAGE,
    USER_REGISTRATION_NOT_SUCCESSFUL,
)

@pytest.mark.usefixtures("setup_teardown")
class TestUserRegistration:

    def setup_method(self):
        self.setup = TestSetup()

    @allure.title("Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание нового пользователя.")
    def test_create_unique_user(self):
        with allure.step("Регистрация нового пользователя"):
            response = self.setup.register_new_user()
            assert response.status_code == 200, UNEXPECTED_STATUS_CODE.format(status_code=response.status_code,
                                                                              response=response.json())
            assert response.json()["success"] is True, USER_REGISTRATION_NOT_SUCCESSFUL

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
            assert response.status_code == 403, UNEXPECTED_STATUS_CODE.format(status_code=response.status_code,
                                                                              response=response.json())
            assert response.json()["success"] is False, REGISTRATION_FAILED
            assert response.json()["message"] == USER_ALREADY_EXISTS, f"Unexpected message: {response.json()['message']}"

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
            assert response.status_code == 403, UNEXPECTED_STATUS_CODE.format(status_code=response.status_code,
                                                                              response=response.json())
            assert response.json()["success"] is False, REGISTRATION_FAILED
            assert response.json()["message"] == MISSING_FIELDS_MESSAGE, f"Unexpected message: {response.json()['message']}"





