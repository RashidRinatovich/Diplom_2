import allure
import pytest
import requests

from message import USER_ALREADY_EXISTS, REQUIRED_FIELDS_ERROR
from urls import Urls
from http import HTTPStatus

from helpers.user_helper import UserHelper


@allure.feature('Создание пользователя')
class TestUserCreation:

    @allure.title('Создание уникального пользователя')
    @allure.description('Проверяем, что можно успешно создать уникального пользователя.')
    def test_create_unique_user_success(self, user):
        """Тест успешного создания уникального пользователя."""
        response = UserHelper.create_user(user)

        assert response.status_code == HTTPStatus.OK
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title('Создание уже существующего пользователя')
    @allure.description('Проверяем, что нельзя создать пользователя, который уже зарегистрирован в системе.')
    def test_create_existing_user_error(self, registered_user):
        """Тест ошибки при создании пользователя, который уже существует."""
        payload = registered_user["payload"]

        with allure.step("POST /api/auth/register — попытка создать уже существующего пользователя"):
            response = requests.post(Urls.CREATE_USER_URL, json=payload)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["success"] is False
        assert response.json()["message"] == USER_ALREADY_EXISTS

    @allure.title('Создание пользователя без обязательного поля')
    @allure.description('Проверяем, что нельзя создать пользователя, если не заполнено одно из обязательных полей.')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_error(self, user, missing_field):
        """Тест ошибки при отсутствии одного из обязательных полей."""
        user.pop(missing_field)
        with allure.step("POST /api/auth/register — создание с пропуском обязательного поля"):
            response = requests.post(Urls.CREATE_USER_URL, json=user)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["success"] is False
        assert response.json()["message"] == REQUIRED_FIELDS_ERROR