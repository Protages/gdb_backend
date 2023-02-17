import os
import base64
import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import games_data


@pytest.mark.order(7)
def test_upload_game_main_image(test_client: TestClient):
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_main_img_valid.png'
    )
    with open(image_path, 'rb') as img_file:
        request_data = {'image': ('game_main_img_valid.png', img_file, 'image/png')}
        response = test_client.post(f'/api/v1/game/{1}/main_img', files=request_data)
    # print('-----', response.json())
    assert response.status_code == 200


def test_upload_game_main_image_invalid_extention(test_client: TestClient):
    response_data = games_data.upload_game_img_invalid_extension
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_invalid.webp'
    )
    with open(image_path, 'rb') as img_file:
        request_data = {'image': ('game_img_invalid.webp', img_file, 'image/png')}
        response = test_client.post(f'/api/v1/game/{1}/main_img', files=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_game_main_image(test_client: TestClient):
    response_content_type = 'image/png'
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_main_img_valid.png'
    )
    with open(image_path, 'rb') as img_file:
        response = test_client.get(f'/api/v1/game/{1}/main_img')
        assert response.content == img_file.read()
    assert response.status_code == 200
    assert response.headers['content-type'] == response_content_type


def test_read_game_main_image_invalid_id(test_client: TestClient):
    response_data = games_data.game_invalid_id_response
    response = test_client.get(f'/api/v1/game/{999}/main_img')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_upload_game_images(test_client: TestClient):
    image_1_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_1_valid.jpg'
    )
    image_2_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_2_valid.jpg'
    )
    with open(image_1_path, 'rb') as img_1_file,\
         open(image_2_path, 'rb') as img_2_file:
        request_data = [
            (
                'images', 
                ('game_img_1_valid.jpg', img_1_file, 'image/jpeg')
            ),
            (
                'images', 
                ('game_img_2_valid.jpg', img_2_file, 'image/jpeg')
            )
        ]
        response = test_client.post(f'/api/v1/game/{1}/images', files=request_data)
    # print('-----', response.json())
    assert response.status_code == 200


def test_upload_game_images_invalid_extension(test_client: TestClient):
    response_data = games_data.upload_game_img_invalid_extension
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_invalid.webp'
    )
    with open(image_path, 'rb') as img_file:
        request_data = [
            (
                'images', 
                ('game_img_invalid.webp', img_file, 'image/webp')
            )
        ]
        response = test_client.post(f'/api/v1/game/{1}/images', files=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_game_images(test_client: TestClient):
    response_content_type = 'application/json'
    image_1_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_1_valid.jpg'
    )
    image_2_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_2_valid.jpg'
    )
    with open(image_1_path, 'rb') as img_1_file,\
         open(image_2_path, 'rb') as img_2_file:
        img_1_base64 = base64.b64encode(img_1_file.read())
        img_2_base64 = base64.b64encode(img_2_file.read())
        
        response = test_client.get(f'/api/v1/game/{1}/images')

        assert len(response.json()) == 2
        assert response.json()[0] == img_1_base64.decode("utf-8") 
        assert response.json()[1] == img_2_base64.decode("utf-8") 
    # print('-----', response.json())
    assert response.status_code == 200
    assert response.headers['content-type'] == response_content_type


def test_upload_game_images_patch(test_client: TestClient):
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_3_valid.jpg'
    )
    with open(image_path, 'rb') as img_file:
        request_data = [
            (
                'images', 
                ('game_img_3_valid.jpg', img_file, 'image/jpg')
            )
        ]
        response = test_client.patch(f'/api/v1/game/{1}/images', files=request_data)
    # print('-----', response.json())
    assert response.status_code == 200


def test_read_game_images_with_patch(test_client: TestClient):
    response_content_type = 'application/json'
    image_1_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_1_valid.jpg'
    )
    image_2_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_2_valid.jpg'
    )
    image_3_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_3_valid.jpg'
    )
    with open(image_1_path, 'rb') as img_1_file,\
         open(image_2_path, 'rb') as img_2_file,\
         open(image_3_path, 'rb') as img_3_file:
        img_1_base64 = base64.b64encode(img_1_file.read())
        img_2_base64 = base64.b64encode(img_2_file.read())
        img_3_base64 = base64.b64encode(img_3_file.read())
        
        response = test_client.get(f'/api/v1/game/{1}/images')

        assert len(response.json()) == 3
        assert response.json()[0] == img_1_base64.decode("utf-8") 
        assert response.json()[1] == img_2_base64.decode("utf-8")
        assert response.json()[2] == img_3_base64.decode("utf-8") 
    # print('-----', response.json())
    assert response.status_code == 200
    assert response.headers['content-type'] == response_content_type


def test_upload_game_images_remove_old_images(test_client: TestClient):
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_1_valid.jpg'
    )
    with open(image_path, 'rb') as img_file:
        request_data = [
            (
                'images', 
                ('game_img_1_valid.jpg', img_file, 'image/jpeg')
            )
        ]
        response = test_client.post(f'/api/v1/game/{1}/images', files=request_data)
    # print('-----', response.json())
    assert response.status_code == 200


def test_read_game_images_after_remove_old_images(test_client: TestClient):
    response_content_type = 'application/json'
    image_path = os.path.join(
        'tests', 'endpoints', 'static', 'games', 'game_img_1_valid.jpg'
    )
    with open(image_path, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read())
        
        response = test_client.get(f'/api/v1/game/{1}/images')

        assert len(response.json()) == 1
        assert response.json()[0] == img_base64.decode("utf-8") 
    # print('-----', response.json())
    assert response.status_code == 200
    assert response.headers['content-type'] == response_content_type
