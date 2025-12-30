import allure
from http import HTTPStatus
from helpers.order_helper import OrderHelper
from message import INGREDIENT_IDS_MUST_BE_PROVIDED


@allure.feature('Создание заказа')
class TestCreateOrder:
    """Тесты для проверки функциональности создания заказа через API."""

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    @allure.description('Проверяем, что авторизованный пользователь может создать заказ с валидными ингредиентами.')
    def test_create_order_with_auth_and_ingredients_success(self, registered_user):
        """Проверка успешного создания заказа с авторизацией и ингредиентами."""
        ingredients = [ingredient["_id"] for ingredient in OrderHelper.get_ingredients()[:3]]
        headers = {"Authorization": registered_user["access_token"]}

        response = OrderHelper.create_order(ingredients, headers)

        assert response.status_code == HTTPStatus.OK
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title('Создание заказа без авторизации с ингредиентами')
    @allure.description('Проверяем, что неавторизованный пользователь может создать заказ с валидными ингредиентами.')
    def test_create_order_without_auth_with_ingredients_success(self):
        """Проверка успешного создания заказа без авторизации, но с ингредиентами."""
        ingredients = [ingredient["_id"] for ingredient in OrderHelper.get_ingredients()[:3]]

        response = OrderHelper.create_order(ingredients)

        assert response.status_code == HTTPStatus.OK
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title('Создание заказа с авторизацией без ингредиентов')
    @allure.description('Проверяем, что нельзя создать заказ без ингредиентов, даже если пользователь авторизован.')
    def test_create_order_with_auth_without_ingredients_error(self, registered_user):
        """Проверка ошибки при создании заказа с авторизацией и без ингредиентов."""
        headers = {"Authorization": registered_user["access_token"]}

        response = OrderHelper.create_order([], headers)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["success"] is False
        assert response.json()["message"] == INGREDIENT_IDS_MUST_BE_PROVIDED

    @allure.title('Создание заказа без авторизации и без ингредиентов')
    @allure.description('Проверяем, что нельзя создать заказ без ингредиентов, если пользователь не авторизован.')
    def test_create_order_without_auth_and_ingredients_error(self):
        """Проверка ошибки при создании заказа без авторизации и без ингредиентов."""
        response = OrderHelper.create_order([])

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["success"] is False
        assert response.json()["message"] == INGREDIENT_IDS_MUST_BE_PROVIDED

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    @allure.description('Проверяем, что система вернет ошибку 500 при попытке создать заказ с неверным хешем ингредиента.')
    def test_create_order_with_invalid_ingredient_hash_error(self, registered_user):
        """Проверка ошибки при создании заказа с неверным хешем ингредиента."""
        ingredients = ["invalid_hash_1", "invalid_hash_2"]
        headers = {"Authorization": registered_user["access_token"]}

        response = OrderHelper.create_order(ingredients, headers)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR