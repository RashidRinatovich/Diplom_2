from http import HTTPStatus

import allure
import requests

from message import EMAIL_OR_PASSWORD_ARE_INCORRECT
from urls import Urls
from helpers.user_generator import UserGenerator


@allure.feature('Авторизация пользователя')
class TestUserLogin:
    """Тесты для проверки функциональности авторизации пользователя через API."""

    @allure.title('Авторизация зарегистрированного пользователя')
    @allure.description('Проверяем, что зарегистрированный пользователь может успешно авторизоваться.')
    def test_login_registered_user_success(self, registered_user):
        """Проверка успешной авторизации зарегистрированного пользователя."""
        creds = {
            "email": registered_user["payload"]["email"],
            "password": registered_user["payload"]["password"],
        }

        with allure.step("POST /api/auth/login — авторизация пользователя"):
            response = requests.post(Urls.LOGIN_USER_URL, json=creds)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["success"] is True

    @allure.title('Авторизация с неверным логином и паролем')
    @allure.description('Проверяем, что пользователь не может авторизоваться с неверными учетными данными.')
    def test_login_incorrect_login_and_password(self):
        """Проверка авторизации с некорректными учетными данными."""
        incorrect_user = UserGenerator.generate_user()

        with allure.step("POST /api/auth/login — авторизация с некорректными данными"):
            response = requests.post(Urls.LOGIN_USER_URL, json=incorrect_user)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["success"] is False
        assert response.json()["message"] == EMAIL_OR_PASSWORD_ARE_INCORRECT