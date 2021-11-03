def test_search_source(client):
    response = client.get('api/search?q=source:brenda&type=pathway')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=source:brenda&type=pathway&offset=0&limit=20&keyword_match=exact',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/1',
                'id': 1,
                'name': 'glycolysis',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_gly',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/3'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/3',
                'id': 3,
                'name': 'cit',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_cit',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/5'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/5',
                'id': 5,
                'name': 'alanine',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_ala',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/7'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/7',
                'id': 7,
                'name': 'leucine',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_leu',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/9'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/9',
                'id': 9,
                'name': 'iso',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_iso',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/11'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/11',
                'id': 11,
                'name': 'met',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_met',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/13'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/13',
                'id': 13,
                'name': 'cas',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_cas',
                'type': 'pathway'
            }],
            'limit':
            20,
            'next':
            None,
            'offset':
            0,
            'previous':
            None,
            'total':
            7
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_source_name(client):
    response = client.get(
        'api/search?q=source:brenda%20name:pw_gly&type=pathway')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=source:brenda name:pw_gly&type=pathway&offset=0&limit=20&keyword_match=exact',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/1',
                'id': 1,
                'name': 'glycolysis',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_gly',
                'type': 'pathway'
            }],
            'limit':
            20,
            'next':
            None,
            'offset':
            0,
            'previous':
            None,
            'total':
            1
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_source_name2(client):
    response = client.get(
        'api/search?q=source:brenda%20name:pw_gly,pw_leu&type=pathway')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=source:brenda name:pw_gly,pw_leu&type=pathway&offset=0&limit=20&keyword_match=exact',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/1',
                'id': 1,
                'name': 'glycolysis',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_gly',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/7'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/7',
                'id': 7,
                'name': 'leucine',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_leu',
                'type': 'pathway'
            }],
            'limit':
            20,
            'next':
            None,
            'offset':
            0,
            'previous':
            None,
            'total':
            2
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_source_name_broad(client):
    response = client.get(
        'api/search?q=source:brenda%20name:gly&type=pathway&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=source:brenda name:gly&type=pathway&offset=0&limit=20&keyword_match=broad',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/1',
                'id': 1,
                'name': 'glycolysis',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_gly',
                'type': 'pathway'
            }],
            'limit':
            20,
            'next':
            None,
            'offset':
            0,
            'previous':
            None,
            'total':
            1
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_source_name_broad2(client):
    response = client.get(
        'api/search?q=source:brenda%20name:gly,leu&type=pathway&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=source:brenda name:gly,leu&type=pathway&offset=0&limit=20&keyword_match=broad',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/1'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/1',
                'id': 1,
                'name': 'glycolysis',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_gly',
                'type': 'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/7'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/7',
                'id': 7,
                'name': 'leucine',
                'reactions': [],
                'source': 'brenda',
                'sourceId': 'pw_leu',
                'type': 'pathway'
            }],
            'limit':
            20,
            'next':
            None,
            'offset':
            0,
            'previous':
            None,
            'total':
            2
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result
