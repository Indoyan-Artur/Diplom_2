import requests
import allure
import pytest
import random

from conftest import URL


@allure.feature("Изменение данных о пользователе")
class TestChangingUserDataApi:
    @allure.title("Изменение данных с авторизацией")
    @pytest.mark.parametrize("field", ["name", "email"])
    def test_data_modification_with_authorization(self, user_creation, authorization, field):
        token = authorization["token"]

        if field == "name":
            new_value = "farid"
        else:
            new_value = f"changed-{random.randint(10000000, 99999999)}@yandex.ru"

        response = requests.patch(f"{URL}/api/auth/user", json={field: new_value}, headers={"Authorization": token})
        assert response.status_code == 200, f"Изменение {field} не прошло: {response.status_code} {response.text}"
        assert response.json()["success"] is True, response.text

        me = requests.get(f"{URL}/api/auth/user", headers={"Authorization": token}, timeout=10)
        assert me.json()["user"][field] == new_value, f"Поле {field} не изменилось: {me.text}"

    @allure.title("Изменение данных без авторизации")
    @pytest.mark.parametrize("field, new_value", [("name", "farid"), ("email", "fdgr@yandex.ru"),])
    def test_changing_data_without_authorization(self, field, new_value):
        response = requests.patch(f"{URL}/api/auth/user", json={field: new_value})
       
        assert response.status_code == 401, f"Изменение {field} прошло: {response.status_code} {response.text}"
        assert response.json()["success"] is False, response.text
        assert response.json()["message"] == "You should be authorised", response.text

