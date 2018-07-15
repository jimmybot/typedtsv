from collections import OrderedDict
import distutils.util
import json
import re

def loads(serialized_data):
    header_info = load_header(serialized_data.readline().strip())
    rows = []
    for line in serialized_data:
        # remove trailing newline, artifact of text file reading
        line = line.rstrip('\n')
        # only process non-empty rows; empty rows are not considered data
        if line:
            row = load_line(header_info, line)
            rows.append(row)
    return header_info, rows

def load_header(line):
    header_info = OrderedDict()
    for column in line.split('\t'):
        col_name, _, col_type = column.partition(':')
        col_type = col_type if col_type else 'str'
        header_info[col_name] = col_type
    return header_info

def load_line(header_info, line, as_dict=False):
    if as_dict:
        cols = OrderedDict()
    else:
        cols = []
    
    ordered_keys = tuple(header_info.keys())

    for i, val in enumerate(line.split('\t')):
        if val == 'null':
            parsed_value = None
        else:
            parsed_value = COL_PARSERS[header_info[ordered_keys[i]]](val)
        if as_dict:
            cols[header_info] = parsed_value
        else:
            cols.append(parsed_value)

    return cols

def dumps(header_info, data, outfile):
    """Serialize a list of rows to a typed tsv file

    header_info may be either a tuple/list of column names and the types will be inferred from the data
    or it may be a full OrderedDictionary whose keys are the column names and values are the column types
    """
    if type(header_info) in (list, tuple):
        header_info = header_info_types_from_row(header_info, data[0])

    raw_header = dump_header(header_info)
    outfile.write(raw_header)
    outfile.write('\n')
    for row in data:
        raw_row = dump_line(header_info, row)
        outfile.write(raw_row)
        outfile.write('\n')

def header_info_types_from_row(names, row):
    header_info = OrderedDict()
    default_type = PYTHON2TYPEDTSV['_']
    for name, col in zip(names, row):
        header_info[name] = PYTHON2TYPEDTSV.get(type(col), default_type)

    return header_info

def dump_header(header_info):
    cols = [] 
    for col_name, col_type in header_info.items():
        cols.append('%s:%s' % (col_name, col_type))
    return '\t'.join(cols)

def dump_line(header_info, row):
    ordered_keys = tuple(header_info.keys())
    raw_cols = []
    for i, col in enumerate(row):
        if col == None:
            raw_col = 'null'
        else:
            raw_col = COL_SERIALIZERS[header_info[ordered_keys[i]]](col)
        raw_cols.append(raw_col)
    return '\t'.join(raw_cols)

def parse_str(raw_str):
    if raw_str == 'null':
        return None
    elif raw_str == '\\null':
        return 'null'
    else:
        return SUB_DECODE_RE.sub(_sub_decode, raw_str)

def dump_str(python_str):
    if python_str == 'null':
        return '\\null'
    else:
        return SUB_ENCODE_RE.sub(_sub_encode, python_str)

def _sub_encode(matchobj):
    return SUB_ENCODE[matchobj.group(0)]

def _sub_decode(matchobj):
    return SUB_DECODE[matchobj.group(0)]

SUB_ENCODE_RE = re.compile(r'\t|\n|\\')
SUB_DECODE_RE = re.compile(r'\\t|\\n|\\\\')

SUB_ENCODE = {
    '\t': '\\t',
    '\n': '\\n',
    '\\': '\\\\',
}

SUB_DECODE = {
    '\\\\': '\\',
    '\\t': '\t',
    '\\n': '\n',
}

# json is fallback serialization method for anything else
PYTHON2TYPEDTSV = {
    int: 'int',
    float: 'float',
    str: 'str',
    bool: 'bool',
    '_': 'json'
}

COL_PARSERS = {
    'int': int,
    'float': float,
    'str': parse_str,
    'json': json.loads,
    'bool': lambda s: bool(distutils.util.strtobool(s)),
}

COL_SERIALIZERS = {
    'int': str,
    'float': str,
    'str': dump_str,
    'json': json.dumps,
    'bool': lambda b: 'true' if b else 'false',
}