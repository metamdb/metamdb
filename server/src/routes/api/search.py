from typing import List, Optional, Tuple, Literal, Union

from flask import Blueprint, json, jsonify, request
from sqlalchemy import and_, or_
from src.errors import handler
from src.models.casm import ReactionSource, Source, ReactionJsonSchema, Pathway, PathwayJsonSchema

search_blueprint = Blueprint('search', __name__, url_prefix='/api/search')
search_blueprint.register_error_handler(handler.InvalidUsage,
                                        handler.handle_invalid_usage)

SEARCH_TYPES = ['reaction', 'pathway']
KEYWORD_MATCHES: List[Union[Literal['exact'],
                            Literal['broad']]] = ['exact', 'broad']


@search_blueprint.route('', methods=['GET'])
def get_search():
    query: Optional[str] = request.args.get('q')
    if not query:
        raise handler.MissingQuery()

    query_type: Optional[str] = request.args.get('type')
    if not query_type:
        raise handler.MissingParameter()

    if query_type.lower() not in SEARCH_TYPES:
        raise handler.BadSearchType(query_type.lower())

    limit: Optional[int] = request.args.get('limit')
    if limit is None:
        limit = 20
    else:
        try:
            limit = int(limit)
        except ValueError:
            limit = 20
        else:
            if limit <= 0 or limit > 50:
                limit = 20

    offset: Optional[int] = request.args.get('offset')
    if offset is not None:
        try:
            offset = int(offset)
        except ValueError:
            offset = 0
    else:
        offset = 0

    keyword_match: Optional[str] = request.args.get('keyword_match')
    if not keyword_match:
        keyword_match = 'exact'
    if keyword_match == 'exact' or keyword_match == 'broad':
        result = get_search_items(query, query_type, limit, offset,
                                  keyword_match)
    else:
        result = get_search_items(query, query_type, limit, offset)

    return jsonify(result)


def get_search_items(query: str,
                     query_type: str,
                     limit: int,
                     offset: int,
                     keyword_match: Literal['exact', 'broad'] = 'exact'):
    search_items = {
        'href':
        f'https://metamdb.tu-bs.de/api/search?q={query}&type={query_type}&offset={offset}&limit={limit}&keyword_match={keyword_match}',
        'offset': offset,
        'limit': limit
    }

    items, total = None, None
    if query_type.lower() == 'reaction':
        items, total = get_reaction_items(query, limit, offset, keyword_match)

    elif query_type.lower() == 'pathway':
        items, total = get_pathway_items(query, limit, offset, keyword_match)

    search_items.setdefault('items', items)
    search_items.setdefault('total', total)

    if offset == 0:
        previous = None
    else:
        diff = offset - limit
        if diff < 0:
            previous = f'https://metamdb.tu-bs.de/api/search?q={query}&type={query_type}&offset={diff}&limit={limit}&keyword_match={keyword_match}'
        else:
            previous = f'https://metamdb.tu-bs.de/api/search?q={query}&type={query_type}&offset={0}&limit={limit}&keyword_match={keyword_match}'

    search_items.setdefault('previous', previous)

    if total is None or total - offset < limit:
        next = None
    else:
        next = f'https://metamdb.tu-bs.de/api/search?q={query}&type={query_type}&offset={offset+limit}&limit={limit}&keyword_match={keyword_match}'

    search_items.setdefault('next', next)

    search_results = None
    if query_type.lower() == 'reaction':
        search_results = {'reactions': search_items}

    elif query_type.lower() == 'pathway':
        search_results = {'pathways': search_items}

    return search_results


def get_pathway_items(
    query: str, limit: int, offset: int, keyword_match: Literal['exact',
                                                                'broad']
) -> Tuple[List["ReactionSource"], Optional[int]]:
    name, source = identify_query(query)

    sql_query = None
    if keyword_match == 'exact':
        if name is not None and source is not None:
            sql_query = Pathway.query.filter(
                and_(Pathway.source_id.in_(name), Pathway.source.in_(source)))

        elif name is not None:
            sql_query = Pathway.query.filter(Pathway.source_id.in_(name))

    else:
        if name is not None and source is not None:
            name = [f'%{element}%' for element in name]
            sql_query = Pathway.query.filter(
                and_(
                    or_(*[Pathway.source_id.like(element)
                          for element in name]), Source.name.in_(source)))

        elif name is not None:
            name = [f'%{element}%' for element in name]
            sql_query = Pathway.query.filter(
                or_(*[Pathway.source_id.like(element) for element in name]))
    if sql_query is None and source is not None:
        sql_query = Pathway.query.filter(Pathway.source.in_(source))

    query_count = None
    items = []
    if sql_query is not None:
        query_count = sql_query.count()

        sql_query = sql_query.limit(limit)
        sql_query = sql_query.offset(offset)
        results = sql_query.all()

        for entry in results:
            if entry:
                json_schema = PathwayJsonSchema()
                json_dump = json_schema.dump(entry)
            else:
                json_dump = None

            items.append(json_dump)

    return items, query_count


def get_reaction_items(
    query: str, limit: int, offset: int, keyword_match: Literal['exact',
                                                                'broad']
) -> Tuple[List["ReactionSource"], Optional[int]]:
    name, source = identify_query(query)

    sql_query = None
    if keyword_match == 'exact':
        if name is not None and source is not None:
            sql_query = ReactionSource.query.join(
                ReactionSource.source).filter(
                    and_(ReactionSource.database_identifier.in_(name),
                         Source.name.in_(source)))

        elif name is not None:
            sql_query = ReactionSource.query.filter(
                ReactionSource.database_identifier.in_(name))

    else:
        if name is not None and source is not None:
            name = [f'%{element}%' for element in name]
            sql_query = ReactionSource.query.join(
                ReactionSource.source).filter(
                    and_(
                        or_(*[
                            ReactionSource.database_identifier.like(element)
                            for element in name
                        ]), Source.name.in_(source)))

        elif name is not None:
            name = [f'%{element}%' for element in name]
            sql_query = ReactionSource.query.filter(
                or_(*[
                    ReactionSource.database_identifier.like(element)
                    for element in name
                ]))
    if sql_query is None and source is not None:
        sql_query = ReactionSource.query.join(ReactionSource.source).filter(
            Source.name.in_(source))

    query_count = None
    items = []
    if sql_query is not None:
        query_count = sql_query.count()

        sql_query = sql_query.limit(limit)
        sql_query = sql_query.offset(limit * offset)
        results = sql_query.all()

        for entry in results:
            if entry.reaction:
                json_schema = ReactionJsonSchema()
                json_dump = json_schema.dump(entry.reaction)
            else:
                json_dump = None

            items.append(json_dump)

    return items, query_count


def identify_query(
        query: str) -> Tuple[Optional[List[str]], Optional[List[str]]]:
    name = None
    source = None

    if ':' in query:
        if ' ' in query:
            split_query = query.split(' ')

            for entry in split_query:
                entry = entry.split(':')

                if entry[0].lower() == 'name':
                    name = entry[1]

                elif entry[0].lower() == 'source':
                    source = entry[1]

        else:
            entry = query.split(':')

            if entry[0].lower() == 'name':
                name = entry[1]

            elif entry[0].lower() == 'source':
                source = entry[1]

    else:
        name = query

    if name is not None:
        name = name.split(',')
    if source is not None:
        source = source.split(',')

    return name, source
