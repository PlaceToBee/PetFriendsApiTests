import os

import pytest

from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password


pf = PetFriends()

#Получаем список питомцев
def test_get_all_pets_with_valid_key(get_key):
    status, result = pf.get_list_of_pets(auth_key=get_key, filter='my_pets')
    assert len(result['pets']) > 0

#Проверяем добавление питомца
def test_post_add_new_pet_with_valid_data(get_key, name='Василий', animal_type='кот', age='4', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
    assert result['name']

#Удаление питомца
def test_delete_successful_delete_self_pet(get_key):
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, 'Петя', 'кот', '7', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)

    _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')
    assert pet_id not in my_pets.values()

#Обновление информации о питомце
def test_put_successful_update_self_info_pet(get_key, name='Даша', animal_type='кошка', age=6):
    _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

#Авторизация с неверным email
def test_api_key_with_not_valid_email(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Авторизация с неверным паролем
def test_api_key_with_not_valid_password(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Авторизация с пустыми полями
def test_api_key_with_not_email_password(email='', password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Авторизация с пустым полем email
def test_api_key_with_not_email(email='', password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Авторизация с пустым полем password
def test_api_key_with_not_password(email=valid_email, password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#Добавление питомца без имени
def test_post_add_new_pet_with_not_name(get_key, name='', animal_type='кот', age='5', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''
    print(result['name'])
    return status, result

#Добавление питомца с отрицательным возрастом
def test_post_add_new_pet_with_negative_age(get_key, name='Антоша', animal_type='кот', age='-5', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
    age = int(result['age'])
    assert status == 200
    assert age < 0
    return status, result

#Добавление питомца с символами в имени
def test_post_add_new_pet_with_not_valid_name(get_key, name='@#$%^', animal_type='кот', age='6', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert result['name'] != ''
    return status, result