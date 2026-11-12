import requests
import allure

from config import API_ORDERS


@allure.feature("Получение информации о заказе")
class TestReceivingOrdersApi:
    @allure.title("Получение заказа авторизованным пользователем")
    def test_receiving_orders_authorized_user(self, user_creation, authorization, ingredient_ids):
        token = authorization["token"]

        create = requests.post(API_ORDERS, json={"ingredients": ingredient_ids}, headers={"Authorization": token},)
        assert create.status_code == 200, f"Создание не прошло: {create.status_code} {create.text}"
        order_number = create.json()["order"]["number"]

        response = requests.get(API_ORDERS, headers={"Authorization": token})
        assert response.status_code == 200, f"Заказы не получены: {response.status_code} {response.text}"
        body = response.json()
        assert body["success"] == True

        numbers = [o["number"] for o in body["orders"]]
        assert order_number in numbers, f"Заказ {order_number} не найден в списке: {response.text}"

    @allure.title("Получение заказа неавторизованным пользователем")
    def test_receiving_orders_unauthorized_user(self):
        response = requests.get(API_ORDERS)

        assert response.status_code == 401, f"Ошибка: {response.status_code} {response.text}"
        assert response.json()["success"] == False