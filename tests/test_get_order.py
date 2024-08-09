import allure
import requests
from project_setup import TestSetup
from urls import ORDERS_URL

class TestOrderRetrieval:

    def setup_method(self):
        self.setup = TestSetup()

    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description("Тест проверяет получение заказов для авторизованного пользователя.")
    def test_get_orders_with_authorization(self):
        # Регистрация нового пользователя и получение токена
        register_response = self.setup.register_new_user()
        assert register_response.status_code == 200, f"Unexpected status code {register_response.status_code}. Response: {register_response.json()}"
        access_token = register_response.json().get("accessToken")
        headers = {"Authorization": access_token}

        # Получаем список ингредиентов
        ingredient_ids = self.setup.get_ingredient_ids()

        # Создаем заказ
        order_payload = {
            "ingredients": ingredient_ids[:1]  # Используем один ингредиент для создания заказа
        }
        order_response = requests.post(ORDERS_URL, json=order_payload, headers=headers)
        assert order_response.status_code == 200, f"Unexpected status code {order_response.status_code}. Response: {order_response.json()}"

        # Получаем список заказов
        orders_response = requests.get(ORDERS_URL, headers=headers)
        assert orders_response.status_code == 200, f"Unexpected status code {orders_response.status_code}. Response: {orders_response.json()}"
        orders_data = orders_response.json()

        # Проверяем, что полученные заказы есть и что они соответствуют ожиданиям
        assert "orders" in orders_data, "Response does not contain 'orders' field"
        assert len(orders_data["orders"]) > 0, "Orders list is empty"

    @allure.title("Получение заказов без авторизации")
    @allure.description("Тест проверяет получение заказов без авторизации.")
    def test_get_orders_without_authorization(self):
        # Получаем список ингредиентов
        ingredient_ids = self.setup.get_ingredient_ids()

        # Создаем заказ
        order_payload = {
            "ingredients": ingredient_ids[:1]  # Используем один ингредиент для создания заказа
        }
        order_response = requests.post(ORDERS_URL, json=order_payload)
        assert order_response.status_code == 200, f"Unexpected status code {order_response.status_code}. Response: {order_response.json()}"

        # Попытка получить список заказов без авторизации
        orders_response = requests.get(ORDERS_URL)
        assert orders_response.status_code == 401, f"Unexpected status code {orders_response.status_code}. Response: {orders_response.json()}"
        assert orders_response.json() == {"success": False, "message": "You should be authorised"}, "Unexpected response for unauthorized access"
