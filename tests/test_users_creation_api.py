import requests
import allure

from test_data import DISPOSABLE_PASSWORD, NAME
from config import API_REGISTER


@allure.feature("Регистрация пользователя")
class TestUsersCreationApi:
    #Данный сценарий не описан в документации, но логически верный, ошибок нет
    @allure.title("Создать уникального пользователя")
    def test_user_creation(self, user_creation):
        response = user_creation["response"]

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("создать пользователя, который уже зарегистрирован")
    def test_creating_existing_user(self, user_creation):
        body = {
            "email": user_creation["email"],
            "password": DISPOSABLE_PASSWORD,
            "name": NAME
        }

        response = requests.post(API_REGISTER, json=body)
       
        assert response.status_code == 403, (f"Создание прошло: {response.status_code} {response.text}")
        assert response.json()["success"] is False
        assert response.json()["message"] == "User already exists"

    @allure.title("создать пользователя и не заполнить одно из обязательных полей")
    def test_registration_without_email(self):
        body = {
            "email": "",
            "password": DISPOSABLE_PASSWORD,
            "name": NAME
        }

        response = requests.post(API_REGISTER, json=body)
       
        assert response.status_code == 403, (f"Создание не прошло: {response.status_code} {response.text}")
        assert response.json()["success"] is False
        assert response.json()["message"] ==  "Email, password and name are required fields"










