# typedtsv
Typed TSV: A simple format for typing TSVs with an implementation in Python 3.

## Why?
JSON, YAML, TOML and other simple formats aren't built for list/table like sets of data.

YAML is particularly slow due to its expansive featureset and JSON, being that is for single objects and not collections, is not chunkable.  I once stored all PyPI package info in a YAML file and reading it back out was going to take half a day.  Using a dead-simple newline-delimited JSON format made parsing take seconds.

Newline-delimited JSON is convenient with little chance of making mistakes in parsing and good performance.  The downsides are the types supported are a bit too limited (no int vs float), and it is also not easily human readable or editable.

TOML is particularly targeted towards configuration files and similarly parses results in a single dictionary object rather than a collection.

CSV/TSV formats have too much ambiguity resulting in repetitive custom parsing logic contained outside the file itself.  CSV quote escaping can also lead to poor parsing performance.

## Goals
- Be simple
- Be fast
- Be easily parallelized
- Be a better alternative to CSV/TSV/JSON and simple uses of YAML

## Non-Goals
- Unlimited extensibility a la YAML
- Config files. Focus is on lists of objects/tabular data

## Format
Format is a normal TSV except the header rows uses a colon format to annotate the type:

`<col_name>:<col_type>\t<col_name2>:<coL_type2>...`

For example:

```
url:str    n_times:int   score:float
https://www.example.com 5   1.6
https://archive.org 99  9.9
```

Initial pass centered around Python's basic types plus JSON.  Current valid types are:

| Type   | Notes                                               |
|--------|------------------------------------------------------
| int    |                                                     |
| float  |                                                     |
| bool   | Valid values: true, false, t, f, yes, no, y, n, 1, 0|
| str    | Newlines, tabs, and backward slash must be escaped  |
| json   |                                                     |
|        |                                                     |
| null   | All types are nullable with value 'null'.  To get literal string null, use '\\null'|

Row separators use `'\n'` only.  Windows line breaks, `'\r\n'` are not valid.

**Gotcha**: In Python, you need to be careful about opening files that may contain Windows newlines:
```py
infile = open('data.ttsv', 'r', newline='\n')   # must set newline='\n' because default for newline is '\n' or '\r' or '\r\n'
```

We'll never allow quoted `'\n'` because this would make the file difficult to chunk and thus make it difficult to parallelize reading.
## TODO:
- ~~Add a boolean type~~
- ~~Add nulls~~
- Add a time type
- Maybe: support array and map types for compatibility with Postgres

## Developing

Make sure you have Poetry installed: https://github.com/sdispater/poetry

```bash
git clone git@github.com:jimmybot/typedtsv.git
cd typedtsv
poetry install
poetry shell
pytest
```
