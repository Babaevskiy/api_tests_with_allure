import pytest
import allure


@allure.feature('Random dog')
@allure.story('Получение фото случайной собаки')
def test_get_random_dog(dog_api):
    response = dog_api.get(path='breeds/image/random')

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        assert response.status_code == 200, f'Неверный код ответа, получен {response.status_code}'

    with allure.step('Десериализуем ответ из json в словарь'):
        response = response.json()
        assert response['status'] == 'success'


@allure.feature('Random dog')
@allure.story('Получение фото случайной собаки определенной породы')
@pytest.mark.parametrize('breed', [
    "afghan",
    "basset",
    "blood",
    "english",
    "ibizan",
    "plott",
    "walker"
])
def test_get_random_breed_image(dog_api, breed):
    response = dog_api.get(path=f'breed/hound/{breed}/images/random')

    with allure.step('Запрос отправлен. Десериализируем ответ из json в словарь'):
        response = response.json()

    assert breed in response['message'], f'Нет ссылки с указанной породой, ответ - {response}'


@allure.feature('List of dog images')
@allure.story('Список фото определенных пород')
@pytest.mark.parametrize('breed', [
    "african",
    "boxer",
    "entlebucher",
    "elkhound",
    "shiba",
    "whippet",
    "spaniel",
    "dvornyaga"
])
def test_get_random_breed_images(dog_api, breed):
    response = dog_api.get(path=f'breed/{breed}/images')

    with allure.step('Запрос отправлен. Десериализируем ответ из json в словарь'):
        response = response.json()

    assert response['status'] == 'success', f'Не удалось получить список изображений породы {breed}'


@allure.feature('List of dog images')
@allure.story('Список определенного количества случайных изображений')
@pytest.mark.parametrize('number_of_images', [i for i in range(0, 51, 10)])
def test_get_few_random_images(dog_api, number_of_images):
    response = dog_api.get(path=f'breeds/image/random/{number_of_images}')

    with allure.step('Запрос отправлен. Десериализируем ответ из json в словарь'):
        response = response.json()

    with allure.step('Посмотрим длину списка со ссылками на фото'):
        final_len = len(response['message'])

    assert final_len == number_of_images, f'Количество фото не {number_of_images}, a {final_len}'
