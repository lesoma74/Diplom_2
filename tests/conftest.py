from project_setup import TestSetup
import pytest

@pytest.fixture(scope="function")
def setup_teardown(request):
    setup = TestSetup()
    request.cls.setup = setup
    setup.setup_method()  # Создаем пользователя
    yield
    setup.teardown_method()  # Удаляем пользователя













