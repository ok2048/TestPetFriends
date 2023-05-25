import json
import requests
import os

from settings import *


class PetFriendsAPI:
    """библиотека API к веб-приложению Pet Friends"""

    def __init__(self):
        # Базовый URL
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """ Метод выполняет GET-запрос к серверу и возвращает статус ответа сервера (status)
        и JSON, содержащий ключ авторизации (key)
        """
        endpoint = '/api/key'
        headers = {'accept': 'application/json', 'email': email, 'password': password}

        res = requests.get(f"{self.base_url}{endpoint}", headers=headers)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: str, filter='') -> json:
        """ Метод выполняет GET-запрос к серверу и возвращает статус ответа сервера (status)
        и JSON, содержащий список питомцев по заданному ключу авторизации (auth_key)
        и фильтру (filter). Допустимые значения фильтра: "" и "my_pets"
        """
        endpoint = '/api/pets'
        headers = {'accept': 'application/json', 'auth_key': auth_key}
        params = {'filter': filter}

        res = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: str, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """ Метод выполняет POST-запрос к серверу с данными нового питомца: кличка (name),
        порода (animal_type), возраст (age) и имя файла с фото (pet_photo).
        Параметр auth_key - ключ аутентификации пользователя.
        Возвращает статус ответа сервера (status) и JSON, содержащий информацию о добавленном питомце,
        в т.ч. ID питомца (id) и ID пользователя-владельца (user_id).
        """
        endpoint = '/api/pets'
        headers = {'accept': 'application/json', 'auth_key': auth_key}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }

        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(f"{self.base_url}{endpoint}", headers=headers, data=data, files=file)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: str, name: str, animal_type: str, age: str) -> json:
        """ Метод выполняет POST-запрос к серверу с данными нового питомца: кличка (name),
        порода (animal_type) и возраст (age).
        Параметр auth_key - ключ аутентификации пользователя.
        Возвращает статус ответа сервера (status) и JSON, содержащий информацию о добавленном питомце,
        в т.ч. ID питомца (id) и ID пользователя-владельца (user_id).
        """
        endpoint = '/api/create_pet_simple'
        headers = {'accept': 'application/json', 'auth_key': auth_key}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(f"{self.base_url}{endpoint}", headers=headers, data=data)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet(self, auth_key: str, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """ Метод выполняет PUT-запрос к серверу с данными для обновления питомца: ID питомца (pet_id), кличка (name),
        порода (animal_type) и возраст (age). Параметр auth_key - ключ аутентификации пользователя.
        Возвращает статус ответа сервера (status) и JSON, содержащий информацию об обновленном питомце,
        в т.ч. ID питомца (id) и ID пользователя-владельца (user_id).
        """
        endpoint = '/api/pets/' + str(pet_id)
        headers = {'accept': 'application/json', 'auth_key': auth_key}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(f"{self.base_url}{endpoint}", headers=headers, data=data)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_photo(self, auth_key: str, pet_id: str, pet_photo: str) -> json:
        """ Метод выполняет POST-запрос к серверу с данными для обновления фото питомца:
        ID питомца (pet_id) и имя файла с фото (pet_photo).
        Параметр auth_key - ключ аутентификации пользователя.
        Возвращает статус ответа сервера (status) и JSON, содержащий информацию об обновленном питомце,
        в т.ч. ID питомца (id) и ID пользователя-владельца (user_id).
        """
        endpoint = '/api/pets/set_photo/' + str(pet_id)
        headers = {'accept': 'application/json', 'auth_key': auth_key}

        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(f"{self.base_url}{endpoint}", headers=headers, files=file)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: str, pet_id: str) -> json:
        """ Метод выполняет DELETE-запрос к серверу с данными для удаления питомца: ID питомца.
        Параметр auth_key - ключ аутентификации пользователя.
        Возвращает статус ответа сервера (status) и JSON, содержащий сообщение об успешном удалении питомца.
        """
        endpoint = '/api/pets/' + str(pet_id)
        headers = {'accept': 'application/json', 'auth_key': auth_key}

        res = requests.delete(f"{self.base_url}{endpoint}", headers=headers)

        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

