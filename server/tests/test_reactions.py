def test_single_id(client):
    response = client.get('/api/reactions/1')
    json_data = response.get_json()

    print(response)
    json_data_result = {
        'balanced':
        False,
        'compounds': [{
            'compound': {
                'id': 1,
                'name': 'fumarate',
                'inchi':
                'InChI=1S/C4H4O4/c5-3(6)1-2-4(7)8/h1-2H,(H,5,6)(H,7,8)/b2-1+',
                'formula': 'C4H4O4'
            },
            'position': 1,
            'quantity': 1,
            'reactant': 'substrate'
        }],
        'externalUrls': {
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

    assert response.status_code == 200
    assert json_data == json_data_result


def test_single_id2(client):
    response = client.get('/api/reactions/2')
    json_data = response.get_json()

    json_data_result = {
        'balanced':
        False,
        'compounds': [],
        'externalUrls': {
            'img': 'https://metamdb.tu-bs.de/img/aam/2',
            'metamdb': 'https://metamdb.tu-bs.de/reaction/2'
        },
        'formula':
        'malate <=> fumarate',
        'href':
        'https://metamdb.tu-bs.de/api/reactions/2',
        'id':
        2,
        'identifiers': [{
            'databaseIdentifier': 'RXN-0543',
            'source': {
                'id': 1,
                'name': 'metacyc'
            }
        }],
        'rxnFile':
        'LARGE RXN FILE',
        'type':
        'reaction',
        'updated':
        True,
        'updatedBy': {
            'id': 1,
            'name': 'Test Name',
            'orcid': '0000-0000-1234-5678',
            'role': {
                'id': 1,
                'name': 'Reviewer'
            }
        },
        'updatedOn':
        None
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_single_wrong_id(client):
    response = client.get('/api/reactions/3')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_single_bad_id(client):
    response = client.get('/api/reactions/thisisanid')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_single_bad_id2(client):
    response = client.get('/api/reactions/$$$$')
    json_data = response.get_json()

    json_data_result = {'message': 'Invalid id'}

    assert response.status_code == 404
    assert json_data == json_data_result


def test_multiple_ids(client):
    response = client.get('/api/reactions?ids=1,2')
    json_data = response.get_json()

    json_data_result = {
        'reactions': [{
            'balanced':
            False,
            'compounds': [{
                'compound': {
                    'id': 1,
                    'name': 'fumarate',
                    'inchi':
                    'InChI=1S/C4H4O4/c5-3(6)1-2-4(7)8/h1-2H,(H,5,6)(H,7,8)/b2-1+',
                    'formula': 'C4H4O4'
                },
                'position': 1,
                'quantity': 1,
                'reactant': 'substrate'
            }],
            'externalUrls': {
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
        }, {
            'balanced':
            False,
            'compounds': [],
            'externalUrls': {
                'img': 'https://metamdb.tu-bs.de/img/aam/2',
                'metamdb': 'https://metamdb.tu-bs.de/reaction/2'
            },
            'formula':
            'malate <=> fumarate',
            'href':
            'https://metamdb.tu-bs.de/api/reactions/2',
            'id':
            2,
            'identifiers': [{
                'databaseIdentifier': 'RXN-0543',
                'source': {
                    'id': 1,
                    'name': 'metacyc'
                }
            }],
            'rxnFile':
            'LARGE RXN FILE',
            'type':
            'reaction',
            'updated':
            True,
            'updatedBy': {
                'id': 1,
                'name': 'Test Name',
                'orcid': '0000-0000-1234-5678',
                'role': {
                    'id': 1,
                    'name': 'Reviewer'
                }
            },
            'updatedOn':
            None
        }]
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_one_wrong(client):
    response = client.get('/api/reactions?ids=1,3')
    json_data = response.get_json()

    json_data_result = {
        'reactions': [{
            'balanced':
            False,
            'compounds': [{
                'compound': {
                    'id': 1,
                    'name': 'fumarate',
                    'inchi':
                    'InChI=1S/C4H4O4/c5-3(6)1-2-4(7)8/h1-2H,(H,5,6)(H,7,8)/b2-1+',
                    'formula': 'C4H4O4'
                },
                'position': 1,
                'quantity': 1,
                'reactant': 'substrate'
            }],
            'externalUrls': {
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
        }, None]
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_all_wrong(client):
    response = client.get('/api/reactions?ids=4,3')
    json_data = response.get_json()

    json_data_result = {'reactions': [None, None]}

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_one_bad(client):
    response = client.get('/api/reactions?ids=1,abc')
    json_data = response.get_json()

    json_data_result = {
        'reactions': [{
            'balanced':
            False,
            'compounds': [{
                'compound': {
                    'id': 1,
                    'name': 'fumarate',
                    'inchi':
                    'InChI=1S/C4H4O4/c5-3(6)1-2-4(7)8/h1-2H,(H,5,6)(H,7,8)/b2-1+',
                    'formula': 'C4H4O4'
                },
                'position': 1,
                'quantity': 1,
                'reactant': 'substrate'
            }],
            'externalUrls': {
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
        }, None]
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_all_bad(client):
    response = client.get('/api/reactions?ids=$$$,abc')
    json_data = response.get_json()

    json_data_result = {'reactions': [None, None]}

    assert response.status_code == 200
    assert json_data == json_data_result


def test_multiple_ids_no_ids(client):
    response = client.get('/api/reactions?ids=')
    json_data = response.get_json()

    json_data_result = {'message': 'Ids are required but none were given'}

    assert response.status_code == 400
    assert json_data == json_data_result


def test_multiple_ids_no_ids2(client):
    response = client.get('/api/reactions?abc=abc')
    json_data = response.get_json()

    json_data_result = {
        'message':
        'The following query parameter/s are required but were not given: [ids]'
    }

    assert response.status_code == 400
    assert json_data == json_data_result


def test_multiple_ids_no_ids3(client):
    response = client.get('/api/reactions')
    json_data = response.get_json()

    json_data_result = {
        'message':
        'The following query parameter/s are required but were not given: [ids]'
    }

    assert response.status_code == 400
    assert json_data == json_data_result