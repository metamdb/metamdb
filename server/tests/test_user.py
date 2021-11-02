def test_single_id(client):
    response = client.get('/api/user/1')
    json_data = response.get_json()

    json_data_result = {
        'history': [{
            'description': 'Changed to number 2',
            'file': 'LARGE RXN FILE 2',
            'id': 1,
            'reaction': {
                'formula':
                'succinate <=> fumarate',
                'id':
                1,
                'identifiers': [{
                    'databaseIdentifier': 'SUC-FUM-OX-RXN',
                    'source': {
                        'id': 1,
                        'name': 'metacyc'
                    }
                }],
                'updated':
                False
            },
            'status': {
                'id': 2,
                'name': 'Approved'
            }
        }],
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