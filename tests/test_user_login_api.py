import requests
import allure

from config import URL, API_AUTH_LOGIN


@allure.feature("Авторизация пользователя")
class TestUserLoginApi:
    @allure.title("Авторизация с валидными данными")
    def test_valid_authorization(self, user_creation, authorization):
        token = authorization["token"]

        assert token.startswith("Bearer "), f"Нет префикса Bearer: {token}"
        assert token.removeprefix("Bearer ").count(".") == 2, f"Похоже не на JWT: {token}"
        assert authorization["response"].status_code == 200, f"Логин не прошёл: {authorization['response'].text}"
        assert authorization["response"].json()["user"]["email"] == user_creation["email"], authorization["response"].text

    @allure.title("Авторизация с некорректным логином и паролем")
    def test_authorization_incorrect_login_and_password(self):
        body = {
        "email": "ivanov@yandex.ru",
        "password": 6447456456
        }
        response = requests.post(API_AUTH_LOGIN, json=body)

        assert response.status_code == 401, f"Ждали 401: {response.status_code} {response.text}" 
        assert response.json()["success"] == False 
        assert response.json()["message"] == "email or password are incorrect"