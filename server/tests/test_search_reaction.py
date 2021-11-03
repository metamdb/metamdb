def test_search_no_hits(client):
    query = 'rxn'
    query_type = 'reaction'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'reactions': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=rxn&type=reaction&offset=0&limit=20&keyword_match=exact',
            'items': [],
            'limit': 20,
            'next': None,
            'offset': 0,
            'previous': None,
            'total': 0
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_one_hit(client):
    query = 'RXN-0543'
    query_type = 'reaction'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'reactions': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=RXN-0543&type=reaction&offset=0&limit=20&keyword_match=exact',
            'items': [{
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


def test_search_one_hit2(client):
    query = 'RXN-0543,HALLO'
    query_type = 'reaction'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'reactions': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=RXN-0543,HALLO&type=reaction&offset=0&limit=20&keyword_match=exact',
            'items': [{
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


def test_search_two_hit_broad(client):
    query = 'rxn'
    query_type = 'reaction'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'reactions': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=rxn&type=reaction&offset=0&limit=20&keyword_match=broad',
            'items': [{
                'compounds': [{
                    'compound': {
                        'id': 1,
                        'name': 'fumarate'
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


def test_search_two_hit_broad2(client):
    query = 'rxn,abc'
    query_type = 'reaction'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'reactions': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=rxn,abc&type=reaction&offset=0&limit=20&keyword_match=broad',
            'items': [{
                'compounds': [{
                    'compound': {
                        'id': 1,
                        'name': 'fumarate'
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
