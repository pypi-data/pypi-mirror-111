#
# hyperdict - Python dictionaries, but on steroids.
#
# Jofin F Archbald
# jofinfab@gmail.com
#
'''
    HYPERDICT\n
    Python dictionaries, but on steroids.\n
    Documentation: https://github.com/j0fiN/hyperdict\n

    `hyperdict` works just like the old dictionary
    but with more additional features.
    It makes working with dictionaries relatively quicker and easier!

    USAGE
    ======================
    Create a hyperdict object
    >>> import hyperdict as hd
    >>> d = hd.HyperDict()


    >>> d[1, 2, 'name'] = None
    HyperDict({1: None, 2: None, 'name': None})

    Using each() function
    >>> -d # empties the dictionary
    >>> d['name', 'age'] = hd.each('Magnus', 31)

    Getters
    >>> d['name', 'age']
    ('Magnus', 31)
    >>> d.change_no_key('No key found!')
    >>> d['name', 'address']
    ('Magnus', 'No key found!')


    Attributes
    >>> d.i # same as list(d.items())
    >>> d.k # same as list(d.keys())
    >>> d.v # same as list(d.values())

    to_hd(*a) function
    >>> a = 1
    >>> b = 24
    >>> c = lambda: 42
    >>> hd.to_hd(a, b, c())
    HyperDict({'a': 1, 'b': 24, 'c': 42})

    Retrieve the keys when values are given
    >>> h(24))
    (('b',),)
    >>> h()
    {1: ('a',), 24: ('b',), 42: ('c', )}
    >>> h.change_no_value('No val found!')
    >>> h(1, 3)
    (('a',), 'No val found!')

    Unary Operators
    >>> ~h # Inversion Operator
    HyperDict({1: 'a', 24: 'b', 42: 'c'})
    >>> +h # Copy operator
    {'a': 1, 'b': 24, 'c': 42}
    >>> -h # Clear operator
    HyperDict({})
'''
from .hyperdict import (
    NoKey,
    NoValue,
    HyperDict,
    each,
    to_hd
)
__version__ = '1.0.0'
__author__ = 'Jofin F Archbald <jofin@gmail.com>'
