# TODO publish and import as external pypi package
# See https://github.com/whummer/csvquerytool

import os
import cmd
import csv
import sys
import json
import logging
import itertools
import six
import sqlite3

_logger = logging.getLogger(__file__)

AUTO_RENAME_DUPLICATE_COLUMN_NAMES = True
DEFAULT_ENCODING = 'UTF-8'
GUESS_TYPE_FROM_N_ROWS = 10000
ROW_PADDING_STRING = ''  # if a row is truncated, missing cells will be filled in with this string


# TODO: sqlite only natively supports the types TEXT, INTEGER, FLOAT, BLOB and NULL.
# Support for extra types, such as datetimes, can be added with the detect_types
# parameter and by registering custom converters with register_converter().
def stripped_string(s):
    return (s or '').strip('%$?').replace(',', '')


CAST_FUNCS = [
    (lambda s: int(stripped_string(s)) if stripped_string(s) != '' else None, 'INTEGER'),
    (lambda s: float(stripped_string(s)) if stripped_string(s) != '' else None, 'FLOAT'),
    (lambda s: s if isinstance(s, str) else s and s.decode(DEFAULT_ENCODING), 'TEXT'),
    (lambda s: s and bytes(s, DEFAULT_ENCODING), 'BLOB')
]

FORMAT_FUNCS = {
    int: lambda x: '%d' % x,
    float: lambda x: ('%f' % x).rstrip('0').rstrip('.'),
}


def sqlite_dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def guess_type(example_data):
    example_data = [e for e in example_data if e is not None]
    for cast_func, cast_type in CAST_FUNCS:
        try:
            list(map(cast_func, example_data))
        except Exception:
            continue
        else:
            return (cast_func, cast_type)
    raise ValueError('Could not guess data type from example data: %r' % example_data)


def rename_duplicates(header):
    for col_num in range(len(header)):
        col_name = header[col_num]
        for n in itertools.count(2):
            if col_name not in header[:col_num]:
                break
            col_name = '%s%d' % (header[col_num], n)
        header[col_num] = col_name
    return header


def create_table_from_csv(csv_file, db_cursor, table_name='csv', header_info='NONE', pad_rows=True):
    _logger.info("Creating table '%s' from CSV file: %s", table_name, csv_file)

    with open(csv_file) as csv_fh:
        reader, tmp_reader = itertools.tee(csv.reader(csv_fh, skipinitialspace=True))
        if header_info == 'USE':
            # If 'USE' first line is header
            header = [col.strip() for col in next(reader)]
        elif header_info == 'IGNORE':
            # If 'IGNORE' first line is not a row (just skip first line) and columns are like: _1, _2, ...
            header = ['_%d' % (i + 1) for i, _ in enumerate(next(reader))]
        else:
            # If 'NONE' first line is a row and columns are like: _1, _2, ...
            header = ['_%d' % (i + 1) for i, _ in enumerate(next(tmp_reader))]
        return create_table(header, reader, db_cursor, table_name, pad_rows=pad_rows)


def create_table_from_json(json_input, db_cursor, table_name='json', pad_rows=True):
    _logger.info("Creating table '%s' from JSON input", table_name)

    if isinstance(json_input, six.string_types):
        with open(json_input) as json_fh:
            json_input = json.loads(json_fh.read())

    header = []
    for item in json_input:
        header.extend([i for i in item.keys() if i not in header])

    def reader():
        def extract(item, column):
            result = item.get(column)
            if result is None:
                return result
            if isinstance(result, (dict, list)):
                result = json.dumps(result)
            result = str(result)
            return result

        for i in json_input:
            item = [extract(i, h) for h in header]
            yield item

    return create_table(header, reader(), db_cursor, table_name, pad_rows=pad_rows)


def create_table(header, reader, db_cursor, table_name, pad_rows=True):

    if not header:
        raise ValueError('First line of CSV file does not contain a valid header with column names')

    if AUTO_RENAME_DUPLICATE_COLUMN_NAMES:
        header = rename_duplicates(header)
    elif len(header) != len(set(header)):
        raise ValueError('CSV file contains duplicate column names')

    # guess the types of each column (by sniffing the first GUESS_TYPE_FROM_N_ROWS rows)
    detect_type_rows = list(itertools.islice(reader, GUESS_TYPE_FROM_N_ROWS))
    guessed_type = dict()
    for col_num, col_name in enumerate(header):
        if pad_rows:
            example_data = [row[col_num] if len(row) > col_num
                else ROW_PADDING_STRING for row in detect_type_rows]
        else:
            try:
                example_data = [row[col_num] for row in detect_type_rows]
            except IndexError:
                raise ValueError('header and data row have different number of columns')
        cast_func, cast_type = guess_type(example_data)
        guessed_type[col_name] = cast_func
    _logger.info('Guessed row types: %r', dict((k, dict(CAST_FUNCS)[v]) for k, v in guessed_type.items()))

    # create the sqlite table
    query_parts = list()
    for col_name in header:
        sqlite_type = dict(CAST_FUNCS)[guessed_type[col_name]]
        query_parts.append('"%s" %s' % (col_name.replace('"', ''), sqlite_type))
    sql = 'CREATE TABLE ' + table_name + ' (' + ', '.join(query_parts) + ')'
    db_cursor.execute(sql)

    # TODO: could do syntax & semantic checking of the SQL query here with an EXPLAIN
    # this would mean an error could be returned quicker, rather than waiting for the data to load
    # see http://stackoverflow.com/questions/2923832/how-do-i-check-sqlite3-syntax

    # insert the data into the table
    num_rows = 0
    for num_rows, row in enumerate(itertools.chain(detect_type_rows, reader)):
        if pad_rows:
            padding = [ROW_PADDING_STRING, ] * max(0, len(header) - len(row))
            row += padding
        elif len(row) != len(header):
            raise ValueError('header and data row have different number of columns')
        sql = 'INSERT INTO %s VALUES (%s)' % (table_name, ','.join('?' for _ in row))
        try:
            data = [guessed_type[col_name](val) for col_name, val in zip(header, row)]
        except ValueError as ex:
            if hasattr(ex, 'encoding'):
                raise ValueError("Not a valid '%s' sequence: %r" % (ex.encoding, ex.object))
            else:
                raise ValueError('Failed to convert row to guessed type, try increasing '
                    'GUESS_TYPE_FROM_N_ROWS to improve guesses: %s' % ex)
        # TODO: this could probably be sped up with db_cursor.executemany()
        db_cursor.execute(sql, data)
    _logger.info('Inserted %d rows', num_rows)


def format_row(row, encoding=DEFAULT_ENCODING):
    """
    Convert a list of mixed elements to a list of strings, formatting
    integers and floats to remove exponent format.
    """
    row_formatted = list()
    for cell in row:
        if isinstance(cell, int):
            row_formatted.append('%d' % cell)
        elif isinstance(cell, float):
            row_formatted.append('%f' % cell)
        else:
            row_formatted.append(str(cell))
    return [cell.encode(encoding) if hasattr(cell, 'encode') else cell for cell in row_formatted]


def choose_table_names(csv_files, based_on_filename=True):
    """
    Function that chooses unique table names for CSV files that are going to be imported. The table names
    are based on the CSV file names if based_on_filename = True, otherwise they are just named "csv", "csv2",
    "csv3", etc.

    TODO: this function should also ensure they are valid SQL table names

    >>> choose_table_names(['/some/path/foo.csv', '/another/path/bar.csv'], based_on_filename=False)
    ['csv', 'csv2']
    >>> choose_table_names(['/some/path/foo.csv', '/another/path/bar.csv'], based_on_filename=True)
    ['foo', 'bar']
    >>> choose_table_names(['/some/path/foobar.csv', '/another/path/foobar.csv'], based_on_filename=True)
    ['foobar', 'foobar2']
    """
    table_names = list()
    for csv_file in csv_files:
        if based_on_filename:
            table_base_name = os.path.splitext(os.path.basename(csv_file))[0]
        else:
            table_base_name = 'csv'
        for n in itertools.count():
            table_name = '%s%d' % (table_base_name, n + 1) if n > 0 else table_base_name
            if table_name not in table_names:
                break
        table_names.append(table_name)
    return table_names


def enable_json_ext(db_conn, quiet=True):
    try:
        db_conn.enable_load_extension(True)
        db_conn.load_extension('json1.so')
    except Exception as e:
        if not quiet:
            _logger.info('Unable to load JSON extensions for SQLite driver: %s' % e)
        pass


def run_query(query, csv_files, output_fh=sys.stdout):
    db_conn = sqlite3.connect(':memory:')
    enable_json_ext(db_conn)
    db_cur = db_conn.cursor()
    table_names = choose_table_names(csv_files, based_on_filename=True)
    for csv_file, table_name in zip(csv_files, table_names):
        create_table(csv_file, db_cur, table_name)
    db_cur.execute(query)
    header = [col[0] for col in db_cur.description]
    writer = csv.writer(output_fh)
    writer.writerow(header)
    for row in db_cur:
        writer.writerow(format_row(row))


class SQLConsole(cmd.Cmd):

    prompt = '=> '

    def __init__(self, db_cur, *args, **kwargs):
        self.db_cur = db_cur
        self._stop = False
        cmd.Cmd.__init__(self, *args, **kwargs)

    def default(self, query):
        if query.endswith('EOF'):
            self._stop = True
            return
        try:
            self.db_cur.execute(query)
        except sqlite3.OperationalError as e:
            print(e)
            return
        header = [col[0] for col in self.db_cur.description]
        writer = csv.writer(sys.stdout)
        writer.writerow(header)
        for row in self.db_cur:
            writer.writerow(format_row(row))

    def emptyline(self):
        self._stop = True

    def postcmd(self, stop, line):
        return self._stop

    def postloop(self):
        print()


def interactive_console(csv_files):
    db_conn = sqlite3.connect(':memory:')
    db_cur = db_conn.cursor()
    table_names = choose_table_names(csv_files, based_on_filename=True)
    for csv_file, table_name in zip(csv_files, table_names):
        create_table(csv_file, db_cur, table_name)
        print("* file '%s' loaded into table '%s'" % (csv_file, table_name))
    console = SQLConsole(db_cur)
    console.cmdloop('SQL Interactive Console')
