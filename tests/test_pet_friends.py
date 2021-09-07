import os

import pytest

from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password


pf = PetFriends()

#Проверяем, что запрос api ключа возвращает код 200 и в результате содержится слово key
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#Проверяем, что запрос всех питомцев возвращает не пустой список
def test_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


#Проверяем, что запрос всех питомцев возвращает не пустой список
def test_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#Проверяем, что можно добавить нового питомца
def test_add_new_pet_with_valid_data(name='Барсик', animal_type='Кот', age='3', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Проверяем, что можно удалить питомца
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Жердяй", "кот", "8", "image/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

#Проверяем, что можно обновить информацию о питомце
def test_successful_update_self_info_pet(name='Милка', animal_type='кошка', age=10):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

#Проверяем авторизацию с неверным email
def test_get_api_key_for_not_valid_user(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Проверяем авторизацию с неверным паролем
def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Проверяем добавление питомца с отрицательным возрастом
def test_add_new_pet_with_not_age(name='Вася', animal_type='Кот', age='-8', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Проверяем добавление питомца без имени
def test_add_new_pet_with_not_name(name='', animal_type='Кот', age='9', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Проверяем добавление питомца в имени с числами, вместо букв
def test_add_new_pet_with_not_valid_name(name='1234567890', animal_type='Кот', age='8', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Проверка авторизации с пустым полем email
def test_get_api_key_for_not_email(email="",password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Проверка авторизации с пустым полем password
def test_get_api_key_for_not_password(email=valid_email, password=""):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result