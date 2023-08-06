import re
import json
import logging
import sqlite3
from localstack.utils.common import load_file
from localstack.utils.aws.aws_responses import convert_to_binary_event_payload
from localstack_ext.utils import csvquerytool

LOG = logging.getLogger(__name__)

DB_NAME_DEFAULT = 's3object'
DB_NAME_GLACIER = 'archive'

REGEX_ID_EXPR = r'[^\s\.\[]+'
REGEX_ARR_STEP = r'\[[^\]]+\]'
REGEX_ARR_ANY = r'\[\*\]'
REGEX_NON_SPACE = r'[^\s]'
REGEX_ATTR_STEP = r'\.%s' % REGEX_ID_EXPR
REGEX_ARR_OR_ATTR_STEP = r'(%s)|(%s)' % (REGEX_ARR_STEP, REGEX_ATTR_STEP)
REGEX_PATH_EXPR = r'%s(%s)+(%s)(%s)*' % (REGEX_ID_EXPR, REGEX_ARR_OR_ATTR_STEP, REGEX_ATTR_STEP, REGEX_ARR_OR_ATTR_STEP)


def convert_to_s3_select_payload(result, event_type=None):
    # see https://docs.aws.amazon.com/AmazonS3/latest/API/RESTSelectObjectAppendix.html
    result = convert_to_binary_event_payload(result)
    return result


def format_s3_select_result(result, serialization_config):
    rows = result.get('rows', [])
    columns = result.get('columns', [])

    csv_config = get_serialization_config(serialization_config, 'CSV')
    json_config = get_serialization_config(serialization_config, 'JSON')

    if csv_config is not None:
        # AWS doesn't print column headers with CSV output
        # TODO use proper csv library
        csv_separator = ', '
        result = '\n'.join([csv_separator.join([str(c) for c in row]) for row in rows])

    elif json_config is not None:
        delimiter = str(json_config.get('RecordDelimiter') or '')

        def convert(row):
            return dict([(columns[i], row[i]) for i in range(len(row))])

        results = [convert(r) for r in rows]
        results = [json.dumps(r) for r in results]
        result = delimiter.join(results)

    return str(result)


def query_csv(query, csv_file, db_name=None, input_serialization=None):
    return run_query(query, csv_file, 'csv', db_name=db_name, input_serialization=input_serialization)


def query_json(query, json_file, db_name=None, input_serialization=None):
    query = rewrite_json_query(query)
    return run_query(query, json_file, 'json', db_name=db_name, input_serialization=input_serialization)


def has_jsonpath_expressions(query):
    regex1 = r'SELECT\s+%s\s+FROM' % REGEX_PATH_EXPR
    regex2 = r'SELECT\s+.*\s+FROM\s+%s' % REGEX_PATH_EXPR
    has_jsonpath = any([re.match(regex, query, re.IGNORECASE) for regex in [regex1, regex2]])
    return bool(has_jsonpath)


def get_serialization_config(configs, key, default=None):
    """ Select key from configs (case insensitively) """
    key = [k for k in configs.keys() if k.lower() == key.lower()]
    if not key:
        return default
    ser_type = key[0]
    if configs[ser_type] is None:
        configs[ser_type] = {}
    return configs[ser_type]


def rewrite_json_query(query):
    # See here for reference: https://www.sqlite.org/json1.html

    query = query.strip()

    # first, determine if the query contains JSONPath queries that need to be rewritten
    has_jsonpath = has_jsonpath_expressions(query)

    # source: SELECT id FROM S3Object[*].Rules[*]
    # target: SELECT json_each.values as id FROM S3Object, json_each(S3Object.Rules)
    regex = r'SELECT\s+(.*)\s+FROM\s+S3Object%s(%s)((%s)+|(\s|$))' % (
        REGEX_ARR_ANY, REGEX_ATTR_STEP, REGEX_ARR_OR_ATTR_STEP)
    if re.match(regex, query, re.IGNORECASE):
        replace = r'SELECT json_each.value\3 AS \1 FROM S3Object, json_each(S3Object\2)'
        query = re.sub(regex, replace, query, flags=re.IGNORECASE)

    # source: SELECT id FROM S3Object[*][*]
    # target: SELECT json_each.values[*] as id FROM S3Object, json_each(S3Object.Rules)
    regex = r'SELECT\s+(.*)\s+FROM\s+S3Object\[\*\]((%s)+)?' % (REGEX_ARR_OR_ATTR_STEP)
    if re.match(regex, query, re.IGNORECASE):
        replace = r'SELECT json_each.value\2 AS \1 FROM S3Object, json_each(S3Object.*)'
        if not has_jsonpath:
            replace = r'SELECT \1 FROM S3Object'
        query = re.sub(regex, replace, query, flags=re.IGNORECASE)

    # source: IS [NOT] MISSING
    # target: IS [NOT] NULL
    regex = r'(.*)IS\s+(NOT\s+)?MISSING'
    if re.match(regex, query, re.IGNORECASE):
        query = re.sub(regex, r'\1IS \2NULL', query, flags=re.IGNORECASE)

    # source: SELECT Rules[*].id AS id FROM S3Object
    # target: SELECT json_extract(Rules, '$[*].id') AS id FROM S3Object
    regex = r'SELECT\s+([^\[\.\s]+(\.[^\s]+))\[[^\]]+\]([^\s]+)'
    if re.match(regex, query, re.IGNORECASE):
        query = re.sub(regex, r"SELECT json_extract(\1, '$\3')", query, flags=re.IGNORECASE)

    # source: SELECT json_each.value.foo.bar.id AS id FROM S3Object
    # target: SELECT json_extract(json_each.value, '$.foo.bar.id') AS id FROM S3Object
    regex = r'SELECT\s+((json_each\.value)|([^\.\s]+))\.([^\s]+(\.[^\s]+)+)'
    if re.match(regex, query, re.IGNORECASE):
        query = re.sub(regex, r"SELECT json_extract(\1, '$.\4')", query, flags=re.IGNORECASE)

    return query


def convert_input(source_file, input_serialization):
    input_serialization = input_serialization or {}
    json_in_type = get_serialization_config(input_serialization, 'JSON', {}).get('Type')
    if json_in_type == 'LINES':
        input_data = load_file(source_file)
        lines = [json.loads(line) for line in input_data.split('\n') if line.strip()]
        return lines
    return source_file


def run_query(query, source_file, source_type, db_name=None, input_serialization=None):
    # simple heuristic to determine table name
    if not db_name:
        for candidate in [DB_NAME_DEFAULT, DB_NAME_GLACIER]:
            if candidate.lower() in query.lower():
                db_name = candidate
                break

    LOG.debug('Using sqlite3 version: %s' % sqlite3.sqlite_version)
    db_conn = sqlite3.connect(':memory:')
    # csvquerytool.enable_json_ext(db_conn)
    db_cur = db_conn.cursor()

    source_input = convert_input(source_file, input_serialization=input_serialization)

    # insert data via util function
    # TODO: implement Parquet format
    if source_type == 'csv':
        header_info = get_serialization_config(input_serialization, 'CSV', {}).get('FileHeaderInfo', 'NONE')
        header_info = header_info.upper()  # convert, e.g., "Use" to "USE"
        csvquerytool.create_table_from_csv(
            source_input, db_cur, db_name, header_info=header_info
        )
    elif source_type == 'json':
        csvquerytool.create_table_from_json(source_input, db_cur, db_name)

    try:
        db_cur.execute(query)
    except sqlite3.OperationalError as e:
        if 'no such column' in str(e):
            # TODO: raise it as AWS error to inform client
            raise Exception('Some headers in query "%s" are missing from the file: %s' % (query, e))
        raise Exception('Unable to run query "%s": %s' % (query, e))
    except Exception as e:
        LOG.info('Unable to run query "%s": %s' % (query, e))
        raise
    columns = [col[0] for col in db_cur.description]
    rows = list(db_cur)
    result = {
        'columns': columns,
        'rows': rows
    }
    return result
