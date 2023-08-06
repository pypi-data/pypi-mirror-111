# `hyperdict`
### *Python dictionaries, but on steroids.*
`hyperdict` works just like the old dictionary but with more additional features. It makes working with dictionaries relatively quicker and easier!

- Built for clean and shorter adders, getters, and setters.

- It significantly reduces the lines of code written for dictionary manipulations.
- Variable names need not be re-written to build the hyperdict ([see here](https://github.com/j0fiN/HyperDict-Python#to_hda-function)).
- `hyperdict` retrieve keys when values are given (value-key pairs). 
- Inbuilt unary operations developed with specific functionalities.
- All inbuilt python dictionary methods work in `hyperdict`.

## Installation
```sh-session
$ pip install hyperdict
---> 100%

# or

$ poetry add hyperdict
---> 100%
```
## User Guide
```python
import hyperdict as hd
```
### Create a hyperdict object
Using the `HyperDict` class, we can build a hyper dictionary.
```python
d = hd.HyperDict()
```
### Basic Usage
Multiple keys can be assigned in a single line.
```python
d[1, 2, 'name'] = None 
# HyperDict({1: None, 2: None, 'name': None})

# without hyperdict
d = {i: None for i in [1, 2, 'name']}
```
Using `each()` function, multiple keys can be assigned with coressponding multiple values.
```python
d['name', 'age', 'skills'] = hd.each('Magnus', 31, ['chess', 'football'])
# HyperDict({'name': 'Magnus', 'age': 31, 'skills': ['chess', 'football']})

# without hyperdict
d['name'] = 'Magnus'
d['age'] = 31
d['skills'] = ['chess', 'football']
```
Multiple values can also be retrieved and can also be delelted using the same syntax.
```python
d['name', 'age']
# ('Magnus', 31)
d['email'] # predefined value for a missing key is None
# None
del d['skills', 'email'] # 'skills' key will be deleted
# trial.py:23: Warning: Missing keys: email
...
... # execution continues after warning...
```
### `hyperdict` as a callable instance
One of the most unique things about hyperdict is value-key retrieval. On accepting value(s) as *arguments*, the hyperdict function return the keys. On calling it without arguments would return a dictionary of all value keys (raises an error if values are not *hashable* types).  
  
The hashable types are cached along with the keys for quicker retrieval from the hyperdict. The cache is cleared when the hyperdict internal dictionary is changed.  
> ***hashable types*** : Namely `int()`, `bool()`, `str()`, `tuple()`, these types in python are hashable since they are *immutable*. They are the types which are allowed to be used as keys in a python dictionary.
```python
d = hd.HyperDict()
d[1, 2, 3] = hd.each(0, 1, 0)
d(0)
# (1, 3)
d(4) # default value for a missing key
# None
d(0, 1)
# ((1, 3), (2,))
d() # return a dict() of all the value-key pairs.
# {0: (1, 3), 1: (2,)}
```
### Attributes and Operators
```python
d.i # same as list(d.items())
d.k # same as list(d.keys())
d.v # same as list(d.values())

inv_d = ~d # Invertor Operation: Returns an Inverts key-values to value-key

# WARNING: This `~` operation works as expected if 
# - values are hashable types (raises an error)
# - values are unique like the keys (overwrites the prev key with a new key.)

cpy_d = +d # Copy Operation: Returns a python dictionary deep-copied from the hyperdict object

-d # Clear Operation: similar to clear() method of python dictionary. Clears the hyperdict dictionary.
```

### Methods and functions.
#### `to_hd(*a)` Function
Creates a `hyperdict` using the variable name as keys.  

You need not write the key names along with values anymore!

> *Warning*: This function does not work in python console, since the nodes from AST are taken as a single expression resulting in None for the expression.
```python
name, age, skills = foo_get_data()

h = hd.to_hd(name, age, skills) 
# HyperDict({'name': 'Magnus', 'age': 24, 'skills': ['chess', 'football']})

# without hyperdict
d = {}
d['name'] = name
d['age'] = age
d['skills'] = skills
```
**`change_no_value(any)`** and **`change_no_key(any)`**: Changes default values for missing key and value(default is `None`).
```python
d.change_no_key('No key found!')
d['name', 'random key']
# ('Magnus', 'No key found!')

d.change_no_value('')
d(24, 'random value')
# (('age',), '')
```
**`hash()`**: Creates hash of the dictionary exclusively.
```python
d.hash() # hash of the dictionary alone.
# 123...
hash(d) # hash of the whole hyperdict instance.
# 321...
```
**`each(*a)`**: Helper function which is used to map the corresponding values to the given keys.
```python
d['name', 'age', 'skill'] = hd.each('Magnus', 31, ['Chess', 'Football'])
```
### Docstrings
```python
import hyperdict as hd
help(hd)
```

## In-built dictionary methods
***All the methods of python inbuilt dictionary works just the same in hyperdict.***


---
## Meta data
### Dependencies
The `to_hd()` function in hyperdict uses [executing](https://github.com/alexmojaki/executing) by [@alexmojaki](https://github.com/alexmojaki) to retrieve object's name and use it as a corresponding key for the value.

### Licence
This project is licensed under the terms of the [Apache License 2.0](https://github.com/j0fiN/HyperDict-Python/blob/main/LICENSE).
### Developement
This package is developed using:
 - [poetry](https://github.com/python-poetry): package and dependency manager.
 - [pytest](https://github.com/pytest-dev): tests.
 - [pcmd](https://j0fin.github.io/pcmd/user_guide.html):  command line shortener.

 The whole wrapper is in a single file `hyperdict.py`.
 ```bash
hyperdict
├── __init__.py
└── hyperdict.py <---
 ```

### Tests
The test file is `test_hyperdict.py`
```bash
tests
├── __init__.py
└── test_hyperdict.py <---
```
`pytest`
```sh-session
$ pcmd run t

# or 

$ poetry run pytest -v
```
`flake8`
```sh-session
$ pcmd run f

# or

$ flake8 hyperdict/ tests/ --ignore=F401,W504
```