# typedtsv
A simple format for typing TSVs with an implementation in Python

## Why?
JSON, YAML, TOML and other simple formats aren't built for list/table like sets of data.  I once stored all PyPI package info in a YAML file and reading it back out was going to take half a day.  Using a dead-simple newline-delimited JSON format made parsing take seconds.

CSV/TSV formats have too much ambiguity resulting in repetitive custom parsing logic contained outside the file itself.

newline-delimited JSON is convenient with little chance of making mistakes in parsing but the types supported are a bit too limited (no int vs float).
It is also not easily human readable or editable.

## Format
Format is a normal TSV except the header rows uses a colon format to annotate the type:

`<col_name>:<col_type>\t<col_name2>:<coL_type2>...`

For example:

```url:str    n_times:int   score:float
https://www.example.com 5   1.6
https://archive.org 99  9.9
```

Initial pass centered around Python's basic types plus JSON.  Current valid types are:
- int
- float
- str
- json

The two modifications for string are newlines and tabs must be escaped.

TODO:
- Add a boolean type
- Add a time type
- Maybe: support array and map types for compatibility with Postgres

## Developing
```bash
git clone git@github.com:jimmybot/typedtsv.git
poetry install
poetry shell
pytest```
