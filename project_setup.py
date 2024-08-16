import requests
import pytest
from string import ascii_lowercase
import random


class TestSetup:
    __test__ = False  # Указываем pytest игнорировать этот класс

    def __init__(self):
        self.base_url = 'https://stellarburgers.nomoreparties.site/api'
        self.created_user = None
        self.access_token = None

    def setup_method(self):
        self.created_user = None
        self.access_token = None

    def teardown_method(self):
        if self.created_user:
            self.delete_user(self.access_token)

    def register_new_user(self, email=None, password=None, name=None):
        email = email or self.generate_random_email()
        password = password or self.generate_random_password()
        name = name or self.generate_random_string(10)

        user_data = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(f"{self.base_url}/auth/register", json=user_data)
        if response.status_code == 200:
            self.created_user = user_data
            self.access_token = response.json().get('accessToken')
        return response

    def login_user(self, email, password):
        login_url = f"{self.base_url}/auth/login"
        response = requests.post(login_url, json={"email": email, "password": password})
        if response.status_code == 200:
            self.access_token = response.json().get('accessToken')
        return response

    def delete_user(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{self.base_url}/auth/user", headers=headers)
        return response

    def update_user(self, token, data):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.patch(f"{self.base_url}/auth/user", json=data, headers=headers)
        return response

    def generate_random_string(self, length):
        letters = ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_random_email(self):
        domain = "example.com"
        random_string = self.generate_random_string(10)
        return f"{random_string}@{domain}"

    def generate_random_password(self):
        return self.generate_random_string(10)

    def create_order(self, ingredients, headers=None):
        # Устанавливаем заголовок по умолчанию, если не указан
        if headers is None:
            headers = {}

        # Если заголовок Authorization не установлен и не требуется, убираем проверку
        if "Authorization" in headers and not headers["Authorization"]:
            raise ValueError("Authorization header is not set. Ensure you have provided the token.")

        # Формируем payload заказа
        order_payload = {
            "ingredients": ingredients
        }

        # Отправляем запрос на создание заказа
        order_url = "https://stellarburgers.nomoreparties.site/api/orders"
        response = requests.post(order_url, json=order_payload, headers=headers)
        return response

    def get_ingredients(self):
        response = requests.get(f"{self.base_url}/ingredients")
        if response.status_code == 200:
            return response.json()
        return response

    def get_ingredient_ids(self):
        ingredients = self.get_ingredients()
        return [ingredient['_id'] for ingredient in ingredients['data']]

    def get_user_orders(self, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = requests.get(f"{self.base_url}/orders", headers=headers)
        return response






