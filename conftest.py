from http import HTTPStatus

import allure
import pytest
import requests
import logging
from helpers.user_generator import UserGenerator
from urls import Urls

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def user():
    """
    Фикстура для генерации данных пользователя и очистки после теста.

    Генерирует данные пользователя, возвращает их в тест.
    В пост-условиях ошибки очистки не "роняют" тест, а логируются.
    """
    with allure.step("Генерация данных для нового пользователя"):
        payload = UserGenerator.generate_user()
    access_token = None

    yield payload

    with allure.step("Очистка: удаление созданного пользователя"):
        login_payload = {"email": payload.get("email"), "password": payload.get("password")}
        if not login_payload.get("email") or not login_payload.get("password"):
            logger.info("Cleanup skipped: missing email/password in payload")
            return

        try:
            with allure.step(f"POST {Urls.LOGIN_USER_URL} | логин для очистки"):
                login_response = requests.post(Urls.LOGIN_USER_URL, json=login_payload)
            if login_response.status_code == HTTPStatus.OK:
                access_token = login_response.json().get("accessToken")
            else:
                logger.warning(
                    "Cleanup login failed: status=%s, body=%s",
                    login_response.status_code,
                    getattr(login_response, "text", ""),
                )
        except requests.exceptions.RequestException:
            logger.exception("Cleanup login request failed due to network/HTTP error")
            return

        if access_token:
            try:
                headers = {"Authorization": access_token}
                with allure.step(f"DELETE {Urls.USER_DATA_URL} | удаление пользователя"):
                    delete_response = requests.delete(Urls.USER_DATA_URL, headers=headers)
                if delete_response.status_code >= 400:
                    logger.warning(
                        "Cleanup delete failed: status=%s, body=%s",
                        delete_response.status_code,
                        getattr(delete_response, "text", ""),
                    )
            except requests.exceptions.RequestException:
                logger.exception("Cleanup delete request failed due to network/HTTP error")
        else:
            logger.info("Cleanup skipped: access token was not obtained")


@pytest.fixture(scope="function")
def registered_user():
    """
    Фикстура для создания и регистрации пользователя в системе.

    Создает пользователя через API, возвращает данные пользователя и токен доступа.
    В пост-условиях ошибки очистки не "роняют" тест, а логируются.
    """
    with allure.step("Создание и регистрация нового пользователя"):
        payload = UserGenerator.generate_user()
        with allure.step(f"POST {Urls.CREATE_USER_URL} | регистрация пользователя"):
            response = requests.post(Urls.CREATE_USER_URL, json=payload)
        assert response.status_code == HTTPStatus.OK
        access_token = response.json().get("accessToken")

    yield {"payload": payload, "access_token": access_token}

    with allure.step("Очистка: удаление зарегистрированного пользователя"):
        if access_token:
            try:
                with allure.step(f"DELETE {Urls.USER_DATA_URL} | удаление пользователя"):
                    delete_response = requests.delete(Urls.USER_DATA_URL, headers={"Authorization": access_token})
                if delete_response.status_code >= 400:
                    logger.warning(
                        "Cleanup delete (registered_user) failed: status=%s, body=%s",
                        delete_response.status_code,
                        getattr(delete_response, "text", ""),
                    )
            except requests.exceptions.RequestException:
                logger.exception("Cleanup delete (registered_user) request failed due to network/HTTP error")
        else:
            logger.info("Cleanup skipped (registered_user): no access token available")