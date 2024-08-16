from project_setup import TestSetup
from utils import generate_random_email, generate_random_password, generate_random_name
import pytest

@pytest.fixture(scope="function")
def setup_teardown(request):
    setup = TestSetup()
    request.cls.setup = setup
    setup.setup_method()  # Создаем пользователя
    yield
    setup.teardown_method()  # Удаляем пользователя


@pytest.fixture
def second_user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name(),
    }










