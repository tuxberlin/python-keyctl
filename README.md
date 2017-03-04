[//]: # (-*- coding: utf-8 -*-)

[![Travis](https://img.shields.io/travis/tuxberlin/python-keyctl/master.svg)](https://travis-ci.org/tuxberlin/python-keyctl)
[![PyPI](https://img.shields.io/pypi/v/keyctl.svg)](https://pypi.python.org/pypi/keyctl)
[![PyPI](https://img.shields.io/pypi/pyversions/keyctl.svg)](https://pypi.python.org/pypi/keyctl)
[![license](https://img.shields.io/github/license/tuxberlin/python-keyctl.svg)](https://raw.githubusercontent.com/tuxberlin/python-keyctl/master/LICENSE)


# python-keyctl

Basic management of keys in the Linux kernel keyring in Python. Also comes with a small gui.


## Table of contents

[//]: # (AUTO TOC BEGIN)

  * [Description](#description)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Module](#module)
    * [GUI](#gui)
  * [Development](#development)
    * [Warning](#warning)
  * [Similar projects](#similar-projects)
  * [License](#license)

[//]: # (AUTO TOC END)


## Description

This is a small library to make use of some functions of the kernel keyring in Python. You can read, add and delete keys.

It simply uses the keyctl command (invoking it via subprocess), so this util must be installed.

Available functions:

 * **list** *(list all keys in keyring)*
 * **describe** *(retrieve key name/description)*
 * **read/pipe/print** *(retrieve key content)*
 * **update** *(modify key content)*
 * **add** *(add key)*
 * **revoke/unlink** *(delete key)*
 * **search/request** *(search for a key by name)*
 * **clear** *(remove all keys from keyring)*

There are many more functions with keys in the kernel keyring (e.g. permissions) that is needed for proper keymanagement. But for my usecase I just needed the given simple functionality. 


## Requirements

Python 2.7
```
$ sudo apt-get install python2.7
$ python --version
Python 2.7.3
```

pip
```
$ sudo apt-get install python-pip
$ pip --version
pip 9.0.1 from .... (python 2.7)
```

The 'keyctl' command
```
$ sudo apt-get install keyutils
$ dpkg -s keyutils | grep Version
Version: 1.5.2-2
```

For the GUI you also need:

Qt4
```
google it for your distribution
```

PySide
```
$ pip install pyside
$ pip show pyside | grep Version
Version: 1.2.4
```


## Installation

```
$ pip install keyctl
```

Ready to use.


## Usage

### Module
Get all keys:
```python
from keyctl import Key
keylist = Key.list()
for mykey in keylist:
    print mykey.id
```

Read existing key:
```python
from keyctl import Key
mykey = Key(123)
print mykey.name
print mykey.data
print mykey.data_hex
```

Find key by name:
```python
from keyctl import Key
mykey = Key.search('test key')
print mykey.id
```

Add key:
```python
from keyctl import Key
mykey = Key.add('test key', 'test content')
print mykey.id
```

Delete key:
```python
from keyctl import Key
mykey = Key(123)
mykey.delete()
```

Update key:
```python
from keyctl import Key
mykey = Key(123)
mykey.update('new content')
```


### GUI
To open the GUI, run the installed command.
```
$ keyctlgui
```


## Development

### Warning

If you run the integrated tests, your user keyring will be cleared. Don't do this when you have active keys e.g. for encryption.


## Similar projects

Similar projects you might want to checkout:

 * https://github.com/sassoftware/python-keyutils (more complete, available in debian repo)
 * https://github.com/jdukes/pykeyctl (more complete, direct library wrapper)


## License

GPL-3.0  
see [LICENSE](https://raw.githubusercontent.com/tuxberlin/python-keyctl/master/LICENSE) file
