import allure
import requests

from urls import Urls


class UserHelper:

    @staticmethod
    @allure.step("Отправка запроса на создание пользователя")
    def create_user(user_data):
        with allure.step(f"POST {Urls.CREATE_USER_URL} | payload={{email, password, name}}"):
            response = requests.post(Urls.CREATE_USER_URL, json=user_data)
        return response