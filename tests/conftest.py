import os
import pytest

from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password


pf = PetFriends()


class TestsUpdated:
    @pytest.fixture(autouse=True)
    def get_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert self.status == 200

    def test_all_pets_with_valid_key(self, filter=''):
        self.status, result = self.pf.get_list_of_pets(self.key, filter)
        assert len(result['pets']) > 0

#Добавление нового питомца
    def test_add_new_pet_with_valid_data(self, get_key, name='Барс', animal_type='кот', age='8', pet_photo='images/cat.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        self.status, result = self.pf.add_new_pet(self.key, name, animal_type, age, pet_photo)
        assert result['name']

#Удаление питомца
    def test_successful_delete_self_pet(self, get_key):
        _, my_pets = self.pf.get_list_of_pets(self.key, "my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(self.key, 'Петя', 'кот', '7', 'images/cat.jpg')
            _, my_pets = self.pf.get_list_of_pets(self.key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        self.status, _ = pf.delete_pet(self.key, pet_id)

        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')
        assert pet_id not in my_pets.values()

#Обновление информации о питомце
    def test_successful_update_self_info_pet(self, get_key, name='Даша', animal_type='кошка', age=6):
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')

        if len(my_pets['pets']) > 0:
            self.status, result = self.pf.update_pet_info(self.key, my_pets['pets'][0]['id'], name, animal_type, age)

            assert self.status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")
