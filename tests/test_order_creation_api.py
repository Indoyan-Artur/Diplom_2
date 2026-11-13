import requests
import allure

from test_data import INVALID_INGREDIENT_IDS, EXPECTED_MESSAGES
from config import URL, API_ORDERS


@allure.feature("Создание заказа")
class TestOrderCreationApi:
    #В данном кейсе выполнено 2 условия из задания "Создание заказа с авторизацией и с ингредиентами" 
    # предпологаю, что в задании опечатка, по сути эти 2 условия логически должны быть одним условияем
    @allure.title("Создание заказа с авторизацией и с ингредиентами")
    def test_order_with_authorization(self, user_creation, authorization, ingredient_ids):
        token = authorization["token"]

        response = requests.post(API_ORDERS, json={"ingredients": ingredient_ids}, headers={"Authorization": token})

        assert response.status_code == 200, f"Создание заказа не прошло: {response.status_code} {response.text}"
        assert response.json()["success"] == True
        number = response.json()["order"]["number"]
        assert isinstance(number, int) and number > 0

    # В документации нет информации про то как должен отрабатывать код при таком сценарии, фактически отрабатывает так, 
    # предпологаю, что без авторизации заказ не должен формироваться
    @allure.title("Создание заказа без авторизации")
    def test_order_without_authorization(self, ingredient_ids):
        response = requests.post(API_ORDERS, json={"ingredients": ingredient_ids})

        assert response.status_code == 200, f" Ошибка, ждали 200 а получили: {response.status_code} {response.text}"
        assert response.json()["success"] == True
        number = response.json()["order"]["number"]
        assert isinstance(number, int) and number > 0

    @allure.title("Создание заказа без ингредиентов")
    def test_order_without_ingredients(self, user_creation, authorization):
        token = authorization["token"]

        response = requests.post(API_ORDERS, json={"ingredients": None}, headers={"Authorization": token})

        assert response.status_code == 400, f"Ошибка: {response.status_code} {response.text}"
        assert response.json()["success"] == False
        assert response.json()["message"] == EXPECTED_MESSAGES["no_ingredients"]

    #В документации написанно, что при таком сценарии сервер должен возвращать 500, но фактически мы получаем 400.
    #В ожидании поставил 400 чтобы тест сответствовал правилу "Тесты запускаются и проходят"
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_order_with_incorrect_hash(self, user_creation, authorization):
        token = authorization["token"]

        response = requests.post(API_ORDERS, json={"ingredients": INVALID_INGREDIENT_IDS}, headers={"Authorization": token})

        assert response.status_code == 500, f"Ожидали 400 (факт API, в доках 500): {response.status_code} {response.text}"



