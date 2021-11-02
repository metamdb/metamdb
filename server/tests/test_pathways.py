def test_single_id_no_reactions(client):
    response = client.get('/api/pathways/1')
    json_data = response.get_json()

    json_data_result = {
        'external_urls': {
            'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
        },
        'href': 'https://metamdb.tu-bs.de/api/pathways/1',
        'name': 'glycolysis',
        'pw_id': 1,
        'reactions': [],
        'source': 'brenda',
        'source_id': 'pw_gly',
        'type': 'pathway'
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_single_id_with_reactions(client):
    response = client.get('/api/pathways/2')
    json_data = response.get_json()

    json_data_result = {
        'external_urls': {
            'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
        },
        'href':
        'https://metamdb.tu-bs.de/api/pathways/2',
        'name':
        'Citric acid cycle',
        'pw_id':
        2,
        'reactions': [{
            'reaction': {
                'external_urls': {
                    'img': 'https://metamdb.tu-bs.de/img/aam/1',
                    'metamdb': 'https://metamdb.tu-bs.de/reaction/1'
                },
                'formula':
                'succinate <=> fumarate',
                'href':
                'https://metamdb.tu-bs.de/api/reactions/1',
                'id':
                1,
                'identifiers': [{
                    'databaseIdentifier': 'SUC-FUM-OX-RXN',
                    'source': {
                        'id': 1,
                        'name': 'metacyc'
                    }
                }],
                'jsonFile': {},
                'rxnFile':
                'LARGE RXN FILE',
                'type':
                'reaction',
                'updated':
                False,
                'updatedBy':
                None,
                'updatedOn':
                None
            }
        }],
        'source':
        'metacyc',
        'source_id':
        'TCA-CYCLE',
        'type':
        'pathway'
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_single_wrong_id(client):
    response = client.get('/api/pathways/3')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_single_bad_id(client):
    response = client.get('/api/pathways/thisisanid')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_single_bad_id2(client):
    response = client.get('/api/pathways/$$$$')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_multiple_ids(client):
    response = client.get('/api/pathways?ids=1,2')
    json_data = response.get_json()

    json_data_result = {
        'pathways': [{
            'external_urls': {
                'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
            },
            'href': 'https://metamdb.tu-bs.de/api/pathways/1',
            'name': 'glycolysis',
            'pw_id': 1,
            'reactions': [],
            'source': 'brenda',
            'source_id': 'pw_gly',
            'type': 'pathway'
        }, {
            'external_urls': {
                'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
            },
            'href':
            'https://metamdb.tu-bs.de/api/pathways/2',
            'name':
            'Citric acid cycle',
            'pw_id':
            2,
            'reactions': [{
                'reaction': {
                    'external_urls': {
                        'img': 'https://metamdb.tu-bs.de/img/aam/1',
                        'metamdb': 'https://metamdb.tu-bs.de/reaction/1'
                    },
                    'formula':
                    'succinate <=> fumarate',
                    'href':
                    'https://metamdb.tu-bs.de/api/reactions/1',
                    'id':
                    1,
                    'identifiers': [{
                        'databaseIdentifier': 'SUC-FUM-OX-RXN',
                        'source': {
                            'id': 1,
                            'name': 'metacyc'
                        }
                    }],
                    'jsonFile': {},
                    'rxnFile':
                    'LARGE RXN FILE',
                    'type':
                    'reaction',
                    'updated':
                    False,
                    'updatedBy':
                    None,
                    'updatedOn':
                    None
                }
            }],
            'source':
            'metacyc',
            'source_id':
            'TCA-CYCLE',
            'type':
            'pathway'
        }]
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_one_wrong(client):
    response = client.get('/api/pathways?ids=1,3')
    json_data = response.get_json()

    json_data_result = {
        'pathways': [{
            'external_urls': {
                'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
            },
            'href': 'https://metamdb.tu-bs.de/api/pathways/1',
            'name': 'glycolysis',
            'pw_id': 1,
            'reactions': [],
            'source': 'brenda',
            'source_id': 'pw_gly',
            'type': 'pathway'
        }, None]
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_all_wrong(client):
    response = client.get('/api/pathways?ids=4,3')
    json_data = response.get_json()

    json_data_result = {'pathways': [None, None]}

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_one_bad(client):
    response = client.get('/api/pathways?ids=1,abc')
    json_data = response.get_json()

    json_data_result = {
        'pathways': [{
            'external_urls': {
                'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
            },
            'href': 'https://metamdb.tu-bs.de/api/pathways/1',
            'name': 'glycolysis',
            'pw_id': 1,
            'reactions': [],
            'source': 'brenda',
            'source_id': 'pw_gly',
            'type': 'pathway'
        }, None]
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_all_bad(client):
    response = client.get('/api/pathways?ids=$$$,abc')
    json_data = response.get_json()

    json_data_result = {'pathways': [None, None]}

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_no_ids(client):
    response = client.get('/api/pathways?ids=')
    json_data = response.get_json()

    json_data_result = {'pathways': [None, None]}


def test_multiple_ids_no_ids2(client):
    response = client.get('/api/pathways?abc=abc')
    json_data = response.get_json()

    json_data_result = {'pathways': [None, None]}


def test_multiple_ids_no_ids3(client):
    response = client.get('/api/pathways')
    json_data = response.get_json()

    json_data_result = {'pathways': [None, None]}
