def test_single_id(client):
    response = client.get('/api/user/1')
    json_data = response.get_json()

    json_data_result = {
        'history': [],
        'user': {
            'id': 1,
            'name': 'Test Name',
            'orcid': '0000-0000-1234-5678',
            'role': {
                'id': 1,
                'name': 'Reviewer'
            }
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_single_wrong_id(client):
    response = client.get('/api/user/2')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_single_bad_id(client):
    response = client.get('/api/user/thisisanid')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_single_bad_id2(client):
    response = client.get('/api/user/$$$$')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result