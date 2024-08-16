import allure
from project_setup import TestSetup
from messages import ORDER_CREATION_NO_INGREDIENTS, ORDER_CREATION_INVALID_INGREDIENTS

class TestOrderCreation:

    def setup_method(self):
        self.setup = TestSetup()

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест проверяет создание заказа с авторизацией в различных сценариях.")
    def test_order_creation_with_authorization(self):
        # Зарегистрируем нового пользователя и получаем токен
        self.register_user_and_create_order()

    @allure.step("Регистрация нового пользователя и получение токена")
    def register_user_and_create_order(self):
        register_response = self.setup.register_new_user()
        assert register_response.status_code == 200, f"Unexpected status code {register_response.status_code}. Response: {register_response.json()}"
        access_token = register_response.json().get("accessToken")
        headers = {"Authorization": access_token}

        # Получаем список ингредиентов
        ingredient_ids = self.setup.get_ingredient_ids()

        # Сценарий 1: Создаем заказ с валидными ингредиентами
        self.create_order_with_valid_ingredients(ingredients=ingredient_ids[:3], headers=headers)

        # Сценарий 2: Создаем заказ без ингредиентов
        self.create_order_without_ingredients(headers=headers)

        # Сценарий 3: Создаем заказ с неверным хешем ингредиентов
        self.create_order_with_invalid_ingredients(headers=headers)

    @allure.step("Создание заказа с валидными ингредиентами")
    def create_order_with_valid_ingredients(self, ingredients, headers):
        order_response = self.setup.create_order(ingredients=ingredients, headers=headers)
        assert order_response.status_code == 200, f"Unexpected status code {order_response.status_code}. Response: {order_response.json()}"
        assert order_response.json().get("success") is True, f"Unexpected response: {order_response.json()}"

    @allure.step("Создание заказа без ингредиентов")
    def create_order_without_ingredients(self, headers):
        order_response_no_ingredients = self.setup.create_order(ingredients=[], headers=headers)
        assert order_response_no_ingredients.status_code == 400, f"Unexpected status code {order_response_no_ingredients.status_code}. Response: {order_response_no_ingredients.json()}"
        assert order_response_no_ingredients.json().get("message") == ORDER_CREATION_NO_INGREDIENTS, f"Unexpected message: {order_response_no_ingredients.json().get('message')}"

    @allure.step("Создание заказа с неверным хешем ингредиентов")
    def create_order_with_invalid_ingredients(self, headers):
        invalid_ingredient_ids = ['invalid_hash_1', 'invalid_hash_2']
        order_response_invalid_hash = self.setup.create_order(ingredients=invalid_ingredient_ids, headers=headers)
        assert order_response_invalid_hash.status_code == 500, f"Unexpected status code {order_response_invalid_hash.status_code}. Response: {order_response_invalid_hash.text}"


class TestOrderCreationWithoutAuthorization:

    def setup_method(self):
        self.setup = TestSetup()

    @allure.title("Создание заказа без авторизации с валидными ингредиентами")
    @allure.description("Тест проверяет создание заказа без авторизации с валидными ингредиентами, невалидными ингредиентами и отсутствием ингредиентов")
    def test_order_creation_without_authorization(self):
        ingredient_ids = self.setup.get_ingredient_ids()

        # Создаем заказ с валидными ингредиентами без авторизации
        order_response = self.setup.create_order(ingredients=ingredient_ids[:3], headers={})
        assert order_response.status_code == 200, f"Unexpected status code {order_response.status_code}. Response: {order_response.json()}"
        order_data = order_response.json()
        assert "order" in order_data, "Response does not contain 'order' field"
        assert order_data.get("success") is True, f"Unexpected response: {order_data}"

        # Создаем заказ с невалидным ID ингредиента без авторизации
        invalid_payload = {
            "ingredients": ["invalid_id"]
        }
        invalid_response = self.setup.create_order(ingredients=invalid_payload["ingredients"], headers={})
        assert invalid_response.status_code == 500, f"Unexpected status code {invalid_response.status_code}. Response: {invalid_response.json()}"

        # Создаем заказ без ингредиентов без авторизации
        empty_payload = {
            "ingredients": []
        }
        empty_response = self.setup.create_order(ingredients=empty_payload["ingredients"], headers={})
        assert empty_response.status_code == 400, f"Unexpected status code {empty_response.status_code}. Response: {empty_response.json()}"
        empty_data = empty_response.json()
        assert empty_data.get("message") == ORDER_CREATION_NO_INGREDIENTS, f"Unexpected message: {empty_data.get('message')}"
