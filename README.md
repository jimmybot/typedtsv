# typedtsv
Typed TSV: A simple format for typing TSVs with an implementation in Python 3.

Available on pypi: https://pypi.org/project/typedtsv/

Install with: `pip install typedtsv`

See code and leave feedback here: https://github.com/jimmybot/typedtsv

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
- Support open data and data sharing/archival. Push information about a dataset into the data file itself for future reproducibility

### Use Cases in Mind
- Database-agnostic, program-agnostic simple file format for open data
- A quick go-to serialization format for sharing reproducible data science datasets
- Easily-created, easily-editable, easily-understood database fixtures for tests

## Non-Goals
- Unlimited extensibility a la YAML
- Config files. Focus is on lists of objects/tabular data

## Format
Format is a normal TSV except the header rows uses a colon format to annotate the type:

`<col_name>:<col_type>\t<col_name2>:<coL_type2>...`

For example:

```
# I'm a comment and will be ignored
url:str    n_times:int   score:float
https://www.example.com 5   1.6
https://archive.org 99  9.9
```

Initial pass centered around Python's basic types plus JSON.  Current valid types are:

| Type     | Notes                                               |
|----------|------------------------------------------------------
| int      |                                                     |
| float    |                                                     |
| bool     | Valid values: true, false, t, f, yes, no, y, n, 1, 0|
| str      | Newlines, tabs, \\, and #  must be escaped           |
| datetime | '2011-01-01 00:00:00' Without timezone assumes UTC  |
| json     |                                                     |
|          |                                                     |
| null     | All types are nullable with value 'null'.  To get literal string 'null', use '\\null'|

Comments are supported, just prefix with #.  Escape actual # in a string with a single backslash '\\#'.

Row separators use `'\n'` only.  Windows line breaks, `'\r\n'` are not valid.

We'll never allow quoted `'\n'` because this would make the file difficult to chunk and thus make it difficult to parallelize reading.

**Gotchas**:
- In Python, you need to be careful about opening files that may contain Windows newlines:
```py
# must set newline='\n' because default for newline is '\n' or '\r' or '\r\n'
infile = open('data.ttsv', 'r', newline='\n')
```
- typedtsv.dumps can infer column types from the first row of your data but not if there are any ```null```'s.  In that case, use the regular OrderedDict method to define column names and types

## TODO:
- ~~Add a boolean type~~
- ~~Add nulls~~
- ~~Add a datetime/date/time type: need to avoid ambiguity yet support common uses~~
- ~~Ergonomics: optionally read and dump single lists of data rather than dealing with a list of lists~~
- Support units annotations such as degrees F, meters/second using similar using same syntax as F#: https://docs.microsoft.com/en-us/dotnet/fsharp/language-reference/units-of-measure
- Maybe: extend format to support column comments / other common metadata
- Maybe: support array and map types for compatibility with Postgres
- Maybe: Support date, time, and/or timeinterval types

## Developing

Make sure you have Poetry installed: https://github.com/sdispater/poetry

```bash
git clone git@github.com:jimmybot/typedtsv.git
cd typedtsv
poetry install
poetry shell
pytest
```
