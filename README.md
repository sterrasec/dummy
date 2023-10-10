# dummy
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/sterrasec/dummy/blob/master/LICENSE)

Generator of static files for testing file upload functionality.

## Motivation


## Installation

Since `dummy` is implemented in Python, it can be installed with the pip command, which is a Python package management system.

```bash
$ pip install git+ssh://git@github.com/sterrasec/dummy.git
```

## Usage

```bash
$ dummy
```

```bash
$ dummy -h
usage: dummy [-h] [-t TEXT] [-b BYTES] file_path

Create a dummy file for testing.

positional arguments:
  file_path             Path to the generated file(.jpeg, .png, .pdf)

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to be written in the file
  -b BYTES, --bytes BYTES
                        Bytes of file(.png only)
```

## License
MIT License
