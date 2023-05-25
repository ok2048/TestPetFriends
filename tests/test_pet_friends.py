import pytest

from api import PetFriendsAPI
from settings import *
import os


class TestPetFriends:
    """ Test Suite для тестирования API Pet Friends
    """

    def setup(self):
        self.pf = PetFriendsAPI()

    def test_get_api_key_for_valid_user(self, email=test_email, password=test_password):
        """ 1. Проверяем, что запрос ключа авторизации возвращает статус 200 и в результате содержится слово key
        при валидном сочетании емэйла и пароля
        """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 200
        assert 'key' in result

    def test_get_all_pets_with_valid_key(self, filter=''):
        """ 2. Проверяем, что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
        запрашиваем список всех питомцев и проверяем, что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо ''
        """

        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']
        status, result = self.pf.get_list_of_pets(auth_key, filter)

        assert status == 200
        assert len(result['pets']) > 0

    def test_successful_add_new_pet_with_valid_data(self, name='Басик', animal_type='кот', age='4',
                                                    pet_photo='images/dobrokot.jpg'):
        """ 3. Проверяем добавление питомца с фото с валидными данными
        """
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Добавляем питомца
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age

    def test_successful_update_self_pet_info(self, name='Доброкот',
                                             animal_type='сибирский кот', age='5'):
        """ 4. Проверяем возможность обновления СВОЕГО питомца валидными данными
        """
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Получаем список своих питомцев
        _, res = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(res['pets']) > 0:
            pet_id = res['pets'][0]['id']
            status, result = self.pf.update_pet(auth_key, pet_id, name, animal_type, age)
            # Проверяем, все ли данные обновились
            assert status == 200
            assert result['name'] == name
            assert result['animal_type'] == animal_type
            assert result['age'] == age
        else:
            raise Exception('Список "Моих питомцев" пуст, некого обновлять')

    def test_successful_add_new_pet_without_photo_valid_data(self, name='Басик', animal_type='кот', age='4'):
        """ 5. Проверяем добавление питомца без фото с валидными данными
        """
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Добавляем питомца
        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age

    def test_successful_update_self_pet_photo(self, pet_photo='images/basik.jpg'):
        """ 6. Проверяем возможность обновления фото СВОЕГО питомца валидными данными
        """
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(res['pets']) > 0:
            pet_id = res['pets'][0]['id']
            old_pet_photo = res['pets'][0]['pet_photo']
            status, result = self.pf.update_pet_photo(auth_key, pet_id, pet_photo)
            assert status == 200
            # Проверяем, что фото обновилось.
            # Хотела сравнить файл {pet_photo} и ответ сервера побайтово, преобразовав с помощью base64,
            # но обнаружилось, что изображение при выгрузке сжимается...
            # Не знаю, предусмотрено ли это документацией, но проверка, то ли изображение выгрузилось,
            # возможна только визуально
            new_pet_photo = result['pet_photo']
            assert old_pet_photo != new_pet_photo
        else:
            raise Exception('Список "Моих питомцев" пуст, некого обновлять')

    def test_successful_delete_self_pet(self):
        """ 7. Проверяем возможность удаления СВОЕГО питомца"""

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и отправляем запрос на удаление
            pet_id = my_pets['pets'][0]['id']
            status, _ = self.pf.delete_pet(auth_key, pet_id)
        else:
            raise Exception('Список "Моих питомцев" пуст, некого удалять')

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()

    def test_unsuccessful_add_pet_with_negative_age(self, name='Басик', animal_type='кот', age='-4'):
        """ 8. Проверяем невозможность записи в поле age отрицательного значения
        """
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Добавляем питомца
        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400

    def test_unsuccessful_add_pet_with_str_age(self, name='Басик', animal_type='кот', age='два'):
        """ 9. Проверяем невозможность записи в поле age строкового значения
        """
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Добавляем питомца
        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400

    def test_unsuccessful_add_pet_with_invalid_key(self, name='Басик', animal_type='кот', age='2'):
        """ 10. Проверяем невозможность добавления питомца с неверным API ключом
        """
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Добавляем питомца, используя неверный API ключ
        status, result = self.pf.add_new_pet_without_photo('wrong' + auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 403

    def test_unsuccessful_get_all_pets_with_invalid_key(self, filter=''):
        """ 11. Проверяем, что запрос всех питомцев возвращает ошибку при неверном API ключе
        """

        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']
        status, result = self.pf.get_list_of_pets('wrong' + auth_key, filter)

        assert status == 403

    def test_unsuccessful_get_all_pets_with_invalid_filter(self, filter='my_cats'):
        """ 12. Проверяем, что запрос всех питомцев возвращает ошибку при невалидном фильтре
        """

        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']
        status, result = self.pf.get_list_of_pets(auth_key, filter)

        assert status != 200

    def test_unsuccessful_update_pet_with_invalid_key(self, name='Доброкот',
                                                      animal_type='сибирский кот', age='5'):
        """ 13. Проверяем невозможность обновления питомца при неверном API ключе
        """
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']

        # Получаем список своих питомцев
        _, res = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(res['pets']) > 0:
            pet_id = res['pets'][0]['id']
            status, result = self.pf.update_pet('wrong' + auth_key, pet_id, name, animal_type, age)
            # Проверяем, все ли данные обновились
            assert status == 403
        else:
            raise Exception('Список "Моих питомцев" пуст, некого обновлять')

    def test_unsuccessful_get_api_key_for_invalid_email(self, email='q1mail.ru', password=test_password):
        """ 14. Проверяем, что запрос ключа авторизации возвращает ошибку при невалидном емэйле
        """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

    def test_unsuccessful_delete_others_pet(self):
        """ 15. Проверяем невозможность удаления ЧУЖОГО питомца"""

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, res = self.pf.get_api_key(test_email, test_password)
        auth_key = res['key']
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Василий", "чеширский кот", "12", "images/cat1.jpg")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        user_id = my_pets['pets'][0]['user_id']

        # Запрашиваем список всех питомцев
        _, my_pets = self.pf.get_list_of_pets(auth_key, '')

        # Ищем чужого питомца
        i = 0
        while my_pets['pets'][i]['user_id'] == user_id:
            i += 1
        pet_id = my_pets['pets'][i]['id']

        status, _ = self.pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список питомцев
        _, my_pets = self.pf.get_list_of_pets(auth_key, '')

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status != 200
        assert pet_id in my_pets.values()

    def teardown(self):
        pass
