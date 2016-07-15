#!/usr/bin/env python3

"""Vector functions for python-gsl."""

# Copyright © 2016 Timothy Pederick.
#
# Based on the GNU Scientific Library (GSL):
#     Copyright © 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
#     2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015 The GSL Team.
#
# This file is part of python-gsl.
#
# python-gsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-gsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-gsl. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['alloc', 'free']

# Standard library imports.
from ctypes import Structure, c_double, c_int, c_size_t, pointer, POINTER
try:
    # Python 3.3+
    from collections.abc import Sequence
except ImportError:
    # Python 3.2 and earlier
    from collections import Sequence

# Local imports.
from . import native, gsl_complex
from .block import gsl_block_p, gsl_block_complex_p
from .errors import exception_from_result

# GSL_ENOMEM error code.
NO_MEMORY = 8

# Native struct definitions.
class gsl_vector(Structure):
    _fields_ = [('size', c_size_t),
                ('stride', c_size_t),
                ('data', POINTER(c_double)),
                ('block', gsl_block_p),
                ('owner', c_int)]

gsl_vector_p = POINTER(gsl_vector)

class gsl_vector_complex(Structure):
    _fields_ = [('size', c_size_t),
                ('stride', c_size_t),
                ('data', POINTER(gsl_complex)),
                ('block', gsl_block_complex_p),
                ('owner', c_int)]

gsl_vector_complex_p = POINTER(gsl_vector_complex)

# Native function declarations.
native.gsl_vector_alloc.argtypes = (c_size_t,)
native.gsl_vector_alloc.restype = gsl_vector_p

native.gsl_vector_calloc.argtypes = (c_size_t,)
native.gsl_vector_calloc.restype = gsl_vector_p

native.gsl_vector_complex_alloc.argtypes = (c_size_t,)
native.gsl_vector_complex_alloc.restype = gsl_vector_complex_p

native.gsl_vector_complex_calloc.argtypes = (c_size_t,)
native.gsl_vector_complex_calloc.restype = gsl_vector_complex_p

def alloc(size, typecode='d', init=False):
    """Allocate a vector in a new memory block."""
    # Use calloc to initialise the new block, or alloc otherwise.
    alloc_fns = {'d': (native.gsl_vector_alloc, native.gsl_vector_calloc),
                 'C': (native.gsl_vector_complex_alloc,
                       native.gsl_vector_complex_calloc)
                 }.get(typecode)
    if alloc_fns is None:
        raise ValueError('unknown type code {!r}'.format(typecode))

    fn_without_init, fn_with_init = alloc_fns

    vector_p = (fn_with_init if init else fn_without_init)(size)
    if not vector_p:
        # Null pointer returned; insufficient memory is available.
        raise exception_from_result(NO_MEMORY)
    else:
        return vector_p


native.gsl_vector_free.argtypes = (gsl_vector_p,)
native.gsl_vector_complex_free.argtypes = (gsl_vector_complex_p,)

def free(vector_p, typecode='d'):
    """Free the memory allocated to a vector."""
    free_fn = {'d': native.gsl_vector_free,
                'C': native.gsl_vector_complex_free
                }.get(typecode)
    if free_fn is None:
        raise ValueError('unknown type code {!r}'.format(typecode))

    free_fn(vector_p)

c_double_p = POINTER(c_double)
native.gsl_blas_ddot.argtypes = (gsl_vector_p, gsl_vector_p, c_double_p)
native.gsl_blas_ddot.restype = c_int

def dot(u, v):
    """Calculate the scalar (dot) product of two vectors."""
    # Construct and initialise a pointer to hold the result.
    result = pointer(c_double(0.0))

    # Call the function and check for errors.
    errcode = native.gsl_blas_ddot(u, v, result)
    if errcode:
        raise exception_from_result(errcode)
    else:
        return result.contents.value

# Pythonic class wrapping vector functionality.
class Vector(Sequence):
    """A vector, or one-dimensional matrix of scalar values."""
    def __init__(self, size, typecode='d'):
        # TODO: Accept an iterable, in place of the size argument, from which
        # the vector will be both sized and initialised.
        self._size = size
        self._typecode = typecode
        self._v_p = alloc(size, typecode=self._typecode, init=True)

    def __del__(self):
        free(self._v_p, self._typecode)

    def __getitem__(self, index):
        # FIXME: This is wrong! There is a native function gsl_vector_get that
        # should be used for this.
        return self._v_p.contents.data[index]

    def __len__(self):
        return self._size

    def __matmul__(self, other):
        """Use the matrix multiplication operator for the dot product."""
        return self.dot(other)

    def dot(self, other):
        return dot(self, other)
