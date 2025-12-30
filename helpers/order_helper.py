import allure
import requests
from urls import Urls


class OrderHelper:

    @staticmethod
    @allure.step("Получение списка доступных ингредиентов")
    def get_ingredients():
        """Получает список доступных ингредиентов."""
        with allure.step(f"GET {Urls.INGREDIENTS_URL}"):
            response = requests.get(Urls.INGREDIENTS_URL)
        return response.json()["data"]

    @staticmethod
    @allure.step("Отправка запроса на создание заказа")
    def create_order(ingredients, headers=None):
        """Создает заказ с указанными ингредиентами и заголовками."""
        payload = {"ingredients": ingredients}
        with allure.step(f"POST {Urls.ORDERS_URL} | payload={payload}"):
            response = requests.post(Urls.ORDERS_URL, json=payload, headers=headers)
        return response