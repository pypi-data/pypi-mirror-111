# Information
TeTest-python is a plugin for user to build the connection to Te-Test testing platform.

## Table of Contents

- [Information](#information)
  - [Table of Contents](#table-of-contents)
  - [Publish](#publish)
  - [Install](#install)
    - [Configration](#configration)
    - [Add paramter for PyTest: conftest.py](#add-paramter-for-pytest-conftestpy)

## Publish
```sh
pip install .
python setup.py sdist build
sudo pip install twine
twine upload dist/*
```

## Install

[pip][]:

```sh
pip install tetest-python && pip freeze > requirements.txt
```

### Configration
```js
{
    "Server": "http://localhost:8080",
    "Token": "",
    "Project": "",
    "TaskID": "",
    "BuildID": "",
    "TimeSpan": "",
    "Paramerter": {},
    "TaskInfo": {},
    "JobInfo": {},
    "Data": [],
    "Report": {
        "ReportGroupName": "TeTest-LocalTest",
        "File": "report.xml",
        "Path": "/",
        "ImagePath": "webdriver_screenshots"
    },
    "Agent": "PYTEST"
}
```

### Add paramter for PyTest: conftest.py
```python
from tetest_python import te_pytest_config

def pytest_addoption(parser):
	# add TE option === Start will support taskid, token, build id for pytest when execute on TE client
	te = te_pytest_config()
	te.pytest_addoption(parser)
	# add TE option === End
```