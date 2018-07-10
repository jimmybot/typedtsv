from collections import OrderedDict
import json

def loads(serialized_data):
    header_info = load_header(serialized_data.readline().strip())
    rows = []
    for line in serialized_data:
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
        parsed_value = COL_PARSERS[header_info[ordered_keys[i]]](val)
        if as_dict:
            cols[header_info] = parsed_value
        else:
            cols.append(parsed_value)

    return cols

def dumps(header_info, data, outfile):
    raw_header = dump_header(header_info)
    outfile.write(raw_header)
    outfile.write('\n')
    for row in data:
        raw_row = dump_line(header_info, row)
        outfile.write(raw_row)
        outfile.write('\n')

def dump_header(header_info):
    cols = []
    for col_name, col_type in header_info.items():
        cols.append('%s:%s' % (col_name, col_type))
    return '\t'.join(cols)

def dump_line(header_info, row):
    ordered_keys = tuple(header_info.keys())
    raw_cols = []
    for i, col in enumerate(row):
        raw_col = COL_SERIALIZERS[header_info[ordered_keys[i]]](col)
        raw_cols.append(raw_col)
    return '\t'.join(raw_cols)

def parse_str(raw_str):
    return raw_str.replace('\\t', '\t').replace('\\n', '\n')

def dump_str(python_str):
    return python_str.replace('\t', '\\t').replace('\n', '\\n')
        
COL_PARSERS = {
    'int': int,
    'float': float,
    'str': parse_str,
    'json': json.loads,
}

COL_SERIALIZERS = {
    'int': str,
    'float': str,
    'str': dump_str,
    'json': json.dumps
}