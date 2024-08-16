import requests
import allure
import pytest
from utils import generate_random_email, generate_random_password, generate_random_name
from urls import BASE_URL
from messages import USER_EMAIL_ALREADY_EXISTS, UNAUTHORIZED

@pytest.fixture
def second_user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name(),
    }

class TestUserModification:
    def setup_method(self):
        self.user_data = {
            "email": generate_random_email(),
            "password": "12345",
            "name": "Пользователь"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=self.user_data)
        assert response.status_code == 200
        self.access_token = response.json()["accessToken"]
        self.headers = {
            "Authorization": self.access_token
        }

    def teardown_method(self):
        # Удаляем пользователя после теста
        if self.access_token:
            response = requests.delete(f"{BASE_URL}/auth/user", headers=self.headers)
            assert response.status_code == 202

    @allure.title("Изменение email пользователя")
    @allure.description("Тест проверяет успешное изменение email пользователя и его корректное отображение.")
    def test_modify_user_email(self):
        with allure.step("Получаем текущие данные пользователя"):
            response = requests.get(f"{BASE_URL}/auth/user", headers=self.headers)
            assert response.status_code == 200
            user_info = response.json()["user"]
            assert user_info["email"] == self.user_data["email"]
            assert user_info["name"] == self.user_data["name"]

        with allure.step("Обновляем email пользователя на случайный"):
            new_email = generate_random_email()
            update_data = {
                "email": new_email,
                "password": self.user_data["password"],
                "name": self.user_data["name"]
            }
            response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=self.headers)
            assert response.status_code == 200
            updated_user_info = response.json()["user"]
            assert updated_user_info["email"] == new_email
            assert updated_user_info["name"] == self.user_data["name"]

        with allure.step("Получаем данные пользователя с обновленным email"):
            response = requests.get(f"{BASE_URL}/auth/user", headers=self.headers)
            assert response.status_code == 200
            user_info = response.json()["user"]
            assert user_info["email"] == new_email
            assert user_info["name"] == self.user_data["name"]

    @allure.title("Изменение email на уже существующий")
    @allure.description("Тест проверяет попытку изменить email на уже существующий, что должно привести к ошибке.")
    def test_modify_user_email_with_existing_email(self, second_user_data):
        with allure.step("Регистрируем второго пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=second_user_data)
            assert response.status_code == 200

        with allure.step("Обновляем email первого пользователя на email второго пользователя"):
            update_data = {
                "email": second_user_data["email"],
                "password": self.user_data["password"],
                "name": self.user_data["name"]
            }
            response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=self.headers)
            assert response.status_code == 403
            assert response.json()["message"] == USER_EMAIL_ALREADY_EXISTS

    @allure.title("Изменение email без авторизации")
    @allure.description("Тест проверяет попытку изменения email без авторизационного токена.")
    def test_modify_user_email_without_token(self):
        with allure.step("Обновляем email пользователя без токена"):
            new_email = generate_random_email()
            update_data = {
                "email": new_email,
                "password": self.user_data["password"],
                "name": self.user_data["name"]
            }
            response = requests.patch(f"{BASE_URL}/auth/user", json=update_data)
            assert response.status_code == 401
            assert response.json()["message"] == UNAUTHORIZED
















