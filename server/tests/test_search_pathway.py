def test_search_no_hits(client):
    query = 'pwy'
    query_type = 'pathway'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pwy&type=pathway&offset=0&limit=20&keyword_match=exact',
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
    query = 'TCA-CYCLE'
    query_type = 'pathway'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=TCA-CYCLE&type=pathway&offset=0&limit=20&keyword_match=exact',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
                },
                'href':
                'https://metamdb.tu-bs.de/api/pathways/2',
                'id':
                2,
                'name':
                'Citric acid cycle',
                'reactions': [{
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
                }],
                'source':
                'metacyc',
                'sourceId':
                'TCA-CYCLE',
                'type':
                'pathway'
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
    query = 'TCA-CYCLE,HALLO'
    query_type = 'pathway'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=TCA-CYCLE,HALLO&type=pathway&offset=0&limit=20&keyword_match=exact',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
                },
                'href':
                'https://metamdb.tu-bs.de/api/pathways/2',
                'id':
                2,
                'name':
                'Citric acid cycle',
                'reactions': [{
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
                }],
                'source':
                'metacyc',
                'sourceId':
                'TCA-CYCLE',
                'type':
                'pathway'
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


def test_search_one_hit_broad(client):
    query = 'cycle'
    query_type = 'pathway'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=cycle&type=pathway&offset=0&limit=20&keyword_match=broad',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
                },
                'href':
                'https://metamdb.tu-bs.de/api/pathways/2',
                'id':
                2,
                'name':
                'Citric acid cycle',
                'reactions': [{
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
                }],
                'source':
                'metacyc',
                'sourceId':
                'TCA-CYCLE',
                'type':
                'pathway'
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


def test_search_one_hit_broad2(client):
    query = 'cycle,abc'
    query_type = 'pathway'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=cycle,abc&type=pathway&offset=0&limit=20&keyword_match=broad',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
                },
                'href':
                'https://metamdb.tu-bs.de/api/pathways/2',
                'id':
                2,
                'name':
                'Citric acid cycle',
                'reactions': [{
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
                }],
                'source':
                'metacyc',
                'sourceId':
                'TCA-CYCLE',
                'type':
                'pathway'
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


def test_search_two_hit(client):
    query = 'TCA-CYCLE,pw_gly'
    query_type = 'pathway'

    response = client.get(f'api/search?q={query}&type={query_type}')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=TCA-CYCLE,pw_gly&type=pathway&offset=0&limit=20&keyword_match=exact',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
                },
                'href':
                'https://metamdb.tu-bs.de/api/pathways/2',
                'id':
                2,
                'name':
                'Citric acid cycle',
                'reactions': [{
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
                }],
                'source':
                'metacyc',
                'sourceId':
                'TCA-CYCLE',
                'type':
                'pathway'
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


def test_search_three_hit_broad(client):
    query = 'cycle,gly'
    query_type = 'pathway'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=cycle,gly&type=pathway&offset=0&limit=20&keyword_match=broad',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/2'
                },
                'href':
                'https://metamdb.tu-bs.de/api/pathways/2',
                'id':
                2,
                'name':
                'Citric acid cycle',
                'reactions': [{
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
                }],
                'source':
                'metacyc',
                'sourceId':
                'TCA-CYCLE',
                'type':
                'pathway'
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/4'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/4',
                'id': 4,
                'name': 'gly',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-gly',
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
            3
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_large_broad(client):
    query = 'pw'
    query_type = 'pathway'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pw&type=pathway&offset=0&limit=20&keyword_match=broad',
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


def test_search_larger_broad(client):
    query = 'pw,rxn'
    query_type = 'pathway'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=0&limit=20&keyword_match=broad',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/4'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/4',
                'id': 4,
                'name': 'gly',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-gly',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/6'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/6',
                'id': 6,
                'name': 'alanine',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-ala',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/8'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/8',
                'id': 8,
                'name': 'leucine',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-leu',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/10'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/10',
                'id': 10,
                'name': 'iso',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-iso',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/12'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/12',
                'id': 12,
                'name': 'met',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-met',
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
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/14'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/14',
                'id': 14,
                'name': 'cas',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-cas',
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
            13
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_larger_broad_limit(client):
    query = 'pw,rxn'
    query_type = 'pathway'

    response = client.get(
        f'api/search?q={query}&type={query_type}&keyword_match=broad&limit=5')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=0&limit=5&keyword_match=broad',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/4'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/4',
                'id': 4,
                'name': 'gly',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-gly',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/6'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/6',
                'id': 6,
                'name': 'alanine',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-ala',
                'type': 'pathway'
            }],
            'limit':
            5,
            'next':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=5&limit=5&keyword_match=broad',
            'offset':
            0,
            'previous':
            None,
            'total':
            13
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_larger_broad_limit_next(client):
    response = client.get(
        'api/search?q=pw,rxn&type=pathway&offset=5&limit=5&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=5&limit=5&keyword_match=broad',
            'items': [{
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/8'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/8',
                'id': 8,
                'name': 'leucine',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-leu',
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
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/10'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/10',
                'id': 10,
                'name': 'iso',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-iso',
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
            }],
            'limit':
            5,
            'next':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=10&limit=5&keyword_match=broad',
            'offset':
            5,
            'previous':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=0&limit=5&keyword_match=broad',
            'total':
            13
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_larger_broad_limit_last(client):
    response = client.get(
        'api/search?q=pw,rxn&type=pathway&offset=10&limit=5&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=10&limit=5&keyword_match=broad',
            'items': [{
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/12'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/12',
                'id': 12,
                'name': 'met',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-met',
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
            }, {
                'externalUrls': {
                    'metamdb': 'https://metamdb.tu-bs.de/pathway/14'
                },
                'href': 'https://metamdb.tu-bs.de/api/pathways/14',
                'id': 14,
                'name': 'cas',
                'reactions': [],
                'source': 'metacyc',
                'sourceId': 'rxn-cas',
                'type': 'pathway'
            }],
            'limit':
            5,
            'next':
            None,
            'offset':
            10,
            'previous':
            'https://metamdb.tu-bs.de/api/search?q=pw,rxn&type=pathway&offset=0&limit=5&keyword_match=broad',
            'total':
            13
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_bad_limit(client):
    limit = -10
    response = client.get(
        f'api/search?q=p&type=pathway&limit={limit}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=0&limit=20&keyword_match=broad',
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


def test_search_bad_limit2(client):
    limit = 'abc'
    response = client.get(
        f'api/search?q=p&type=pathway&limit={limit}&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=0&limit=20&keyword_match=broad',
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


def test_search_bad_limit3(client):
    response = client.get(
        'api/search?q=p&type=pathway&limit&keyword_match=broad')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=0&limit=20&keyword_match=broad',
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


def test_search_offset_too_low(client):
    offset = -5
    response = client.get(
        f'api/search?q=p&type=pathway&limit=5&offset={offset}&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=-5&limit=5&keyword_match=broad',
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
            }],
            'limit':
            5,
            'next':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=0&limit=5&keyword_match=broad',
            'offset':
            -5,
            'previous':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=-10&limit=5&keyword_match=broad',
            'total':
            7
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_offset_too_high(client):
    offset = 100
    response = client.get(
        f'api/search?q=p&type=pathway&limit=5&offset={offset}&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=100&limit=5&keyword_match=broad',
            'items': [],
            'limit': 5,
            'next': None,
            'offset': 100,
            'previous':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=0&limit=5&keyword_match=broad',
            'total': 7
        }
    }

    assert response.status_code == 200
    assert json_data == json_data_result


def test_search_bad_offset(client):
    offset = 'abc'
    response = client.get(
        f'api/search?q=p&type=pathway&limit=5&offset={offset}&keyword_match=broad'
    )
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=0&limit=5&keyword_match=broad',
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
            }],
            'limit':
            5,
            'next':
            'https://metamdb.tu-bs.de/api/search?q=p&type=pathway&offset=5&limit=5&keyword_match=broad',
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


def test_search_bad_keyword_match(client):
    response = client.get(
        'api/search?q=pw_gly&type=pathway&limit=1&offset=0&keyword_match=abc')
    json_data = response.get_json()

    json_data_result = {
        'pathways': {
            'href':
            'https://metamdb.tu-bs.de/api/search?q=pw_gly&type=pathway&offset=0&limit=1&keyword_match=exact',
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
            1,
            'next':
            'https://metamdb.tu-bs.de/api/search?q=pw_gly&type=pathway&offset=1&limit=1&keyword_match=exact',
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


def test_search_bad_type(client):
    response = client.get('api/search?q=pw_gly&type=abc')
    json_data = response.get_json()

    json_data_result = {'message': 'Bad search type field abc'}

    assert response.status_code == 400
    assert json_data == json_data_result

def test_search_no_type(client):
    response = client.get('api/search?q=pw_gly')
    json_data = response.get_json()

    json_data_result = {'message': 'Missing parameter type'}

    assert response.status_code == 400
    assert json_data == json_data_result

def test_search_no_query(client):
    response = client.get('api/search?type=pathway')
    json_data = response.get_json()

    json_data_result = {'message': 'No search query'}

    assert response.status_code == 400
    assert json_data == json_data_result

def test_search_no_type_no_query(client):
    response = client.get('api/search')
    json_data = response.get_json()

    json_data_result = {'message': 'No search query'}

    assert response.status_code == 400
    assert json_data == json_data_result