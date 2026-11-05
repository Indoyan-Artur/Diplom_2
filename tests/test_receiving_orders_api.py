import requests
import allure

from conftest import URL

@allure.feature("Получение информации о заказе")
class TestReceivingOrdersApi:
    @allure.title("Получение заказа авторизованным пользователем")
    def test_receiving_orders_authorized_user(self, user_creation, authorization, ingredient_ids):
        token = authorization["token"]

        create = requests.post(f"{URL}/api/orders", json={"ingredients": ingredient_ids}, headers={"Authorization": token},)
        assert create.status_code == 200, f"Создание не прошло: {create.status_code} {create.text}"
        order_number = create.json()["order"]["number"]

        response = requests.get(f"{URL}/api/orders", headers={"Authorization": token})
        assert response.status_code == 200, f"Заказы не получены: {response.status_code} {response.text}"
        body = response.json()
        assert body["success"] == True

        numbers = [o["number"] for o in body["orders"]]
        assert order_number in numbers, f"Заказ {order_number} не найден в списке: {response.text}"

    @allure.title("Получение заказа неавторизованным пользователем")
    def test_receiving_orders_unauthorized_user(self):
        response = requests.get(f"{URL}/api/orders")

        assert response.status_code == 401, f"Ошибка: {response.status_code} {response.text}"
        assert response.json()["success"] == False