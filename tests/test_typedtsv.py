import io
import toml

from typedtsv import __version__
from typedtsv.typedtsv import *

def test_version_in_sync():
    assert toml.load('pyproject.toml')['tool']['poetry']['version'] == __version__

def test_load_header():
    assert OrderedDict((
        ('title', 'str'),
        ('url', 'str'),
        ('n_loads', 'int'),
    )) == load_header('title:str\turl:str\tn_loads:int')

def test_load_line():
    header_info = load_header('one:float\ttwo:int\tthree:json\tfour:str\tfive:str')
    line = '1\t1\t{"dragonfruit": "huolongguo"}\t大驚小怪\t5'
    assert [
        1.0,
        1,
        {"dragonfruit": "huolongguo"},
        "大驚小怪",
        "5",
    ] == load_line(header_info, line)

def test_dump_header():
    header_info = OrderedDict((
        ('one', 'int'),
        ('two', 'str')
    ))

    assert 'one:int\ttwo:str' == dump_header(header_info)

def test_dump_line():
    header_info = OrderedDict((
        ('one', 'int'),
        ('two', 'str')
    ))
    assert '99\tgreen\\t+\\tblue\\n=grue' == dump_line(header_info, (
        99,
        'green\t+\tblue\n=grue'
    ))

def test_header_roundtrip():
    raw_header = 'title:str\turl:str\tn_loads:int'
    header_info = load_header(raw_header)
    raw_header_roundtrip = dump_header(header_info)
    assert raw_header == raw_header_roundtrip

def test_line_roundtrip():
    header_info = OrderedDict((
        ('one', 'int'),
        ('two', 'str')
    ))
    parsed_data = [
        99,
        'green\t+\tblue\n=grue\\t\\n\\ \\\\'
    ]
    assert parsed_data == load_line(header_info, dump_line(header_info, parsed_data))

def test_loads():
    raw_data = io.StringIO()
    raw_data.write('title:str\turl:str\tn_loads:int\n')
    raw_data.write('0\thttps://biglittlebear.cc\t55\n')
    raw_data.seek(0)
    header_info, rows = loads(raw_data)
    assert OrderedDict((
        ('title', 'str'),
        ('url', 'str'),
        ('n_loads', 'int'),
    )) == header_info

    assert [
        ['0', 'https://biglittlebear.cc', 55],
    ] == rows

def test_load_bool_true():
    raw_data = io.StringIO()
    raw_data.write('title:str\tfetched:bool\n')
    raw_data.write('0\ttrue\n')
    raw_data.write('1\tt\n')
    raw_data.write('2\tyes\n')
    raw_data.write('3\ty\n')
    raw_data.write('4\ton\n')
    raw_data.write('5\t1\n')
    raw_data.seek(0)
    header_info, rows = loads(raw_data)
    for row in rows:
        assert True == row[1]

def test_load_bool_false():
    raw_data = io.StringIO()
    raw_data.write('title:str\tfetched:bool\n')
    raw_data.write('0\tfalse\n')
    raw_data.write('1\tf\n')
    raw_data.write('2\tno\n')
    raw_data.write('3\tn\n')
    raw_data.write('4\toff\n')
    raw_data.write('5\t0\n')
    raw_data.seek(0)
    header_info, rows = loads(raw_data)
    for row in rows:
        assert False == row[1]

def test_dumps():
    header_info = OrderedDict((
        ('title', 'str'),
        ('url', 'str'),
        ('n_loads', 'int'),
    ))
    data = [
        ['0', 'https://biglittlebear.cc', 55],
    ]
    outfile = io.StringIO()
    dumps(header_info, data, outfile)
    outfile.seek(0)
    raw_data_dumped = outfile.read()
    raw_data_expected = (
        'title:str\turl:str\tn_loads:int\n'
        '0\thttps://biglittlebear.cc\t55\n'
    )

    assert raw_data_expected == raw_data_dumped

def test_dump_roundtrip():
    header_info = OrderedDict((
        ('title', 'str'),
        ('url', 'str'),
        ('n_loads', 'int'),
        ('in_cache', 'bool'),
    ))
    data = [
        ['0', 'https://biglittlebear.cc', 55, True],
        ['1', 'https://archive.org', 99, False],
    ]
    outfile = io.StringIO()
    dumps(header_info, data, outfile)
    outfile.seek(0)
    parsed_header_info, parsed_data = loads(outfile)
    assert header_info == parsed_header_info
    assert data == parsed_data

def test_dump_roundtrip_slashn():
    header_info = OrderedDict((
        ('title', 'str'),
        ('url', 'str'),
        ('n_loads', 'int'),
    ))
    data = [
        ['chit \n neng \t sah \\n', 'https://biglittlebear.cc', 55],
    ]
    outfile = io.StringIO()
    dumps(header_info, data, outfile)
    outfile.seek(0)
    parsed_header_info, parsed_data = loads(outfile)
    assert header_info == parsed_header_info
    assert data == parsed_data

def test_dump_roundtrip_windowsnewline():
    header_info = OrderedDict((
        ('title', 'str'),
        ('url', 'str'),
        ('n_loads', 'int'),
    ))
    data = [
        ['chit \r\n \n neng \t sah \\n', 'https://biglittlebear.cc', 55],
    ]
    # regular files need to be opened with newline='\n'
    # io.StringIO has a good default to only recognize '\n'
    outfile = io.StringIO(newline='\n')
    dumps(header_info, data, outfile)
    outfile.seek(0)
    parsed_header_info, parsed_data = loads(outfile)
    assert header_info == parsed_header_info
    assert data == parsed_data
