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

__all__ = ['Vector']

# Standard library imports.
from ctypes import (ArgumentError, Structure, c_double, c_int, c_size_t,
                    pointer, POINTER)
try:
    # Python 3.3+
    from collections.abc import Iterable, Sequence
except ImportError:
    # Python 3.2 and earlier
    from collections import Iterable, Sequence
from numbers import Real

# Third-party library imports (bundled with python-gsl).
from . import finalize

# Local imports.
from . import native, gsl_complex
from .block import gsl_block_p, gsl_block_complex_p
from .errors import exception_from_result

# GSL_ENOMEM error code.
NO_MEMORY = 8

# Native type and struct definitions.
c_double_p = POINTER(c_double)
gsl_complex_p = POINTER(gsl_complex)

class gsl_vector(Structure):
    _fields_ = [('size', c_size_t),
                ('stride', c_size_t),
                ('data', c_double_p),
                ('block', gsl_block_p),
                ('owner', c_int)]

gsl_vector_p = POINTER(gsl_vector)

class gsl_vector_complex(Structure):
    _fields_ = [('size', c_size_t),
                ('stride', c_size_t),
                ('data', gsl_complex_p),
                ('block', gsl_block_complex_p),
                ('owner', c_int)]

gsl_vector_complex_p = POINTER(gsl_vector_complex)

# Native memory-allocation function declarations.
native.gsl_vector_alloc.argtypes = (c_size_t,)
native.gsl_vector_alloc.restype = gsl_vector_p

native.gsl_vector_calloc.argtypes = (c_size_t,)
native.gsl_vector_calloc.restype = gsl_vector_p

native.gsl_vector_complex_alloc.argtypes = (c_size_t,)
native.gsl_vector_complex_alloc.restype = gsl_vector_complex_p

native.gsl_vector_complex_calloc.argtypes = (c_size_t,)
native.gsl_vector_complex_calloc.restype = gsl_vector_complex_p

# Native memory-deallocation function declarations.
native.gsl_vector_free.argtypes = (gsl_vector_p,)
native.gsl_vector_complex_free.argtypes = (gsl_vector_complex_p,)

# Native element-access function declarations.
native.gsl_vector_get.argtypes = (gsl_vector_p, c_size_t)
native.gsl_vector_get.restype = c_double
native.gsl_vector_complex_get.argtypes = (gsl_vector_complex_p, c_size_t)
native.gsl_vector_complex_get.restype = gsl_complex

native.gsl_vector_set.argtypes = (gsl_vector_p, c_size_t, c_double)
native.gsl_vector_complex_set.argtypes = (gsl_vector_complex_p, c_size_t,
                                          gsl_complex)

native.gsl_vector_memcpy.argtypes = (gsl_vector_p, gsl_vector_p)
native.gsl_vector_memcpy.restype = c_int
native.gsl_vector_complex_memcpy.argtypes = (gsl_vector_complex_p,
                                             gsl_vector_complex_p)
native.gsl_vector_complex_memcpy.restype = c_int

# Native vector-operation function declarations.
native.gsl_vector_add.argtypes = (gsl_vector_p, gsl_vector_p)
native.gsl_vector_add.restype = c_int
native.gsl_vector_complex_add.argtypes = (gsl_vector_complex_p,
                                          gsl_vector_complex_p)
native.gsl_vector_complex_add.restype = c_int

native.gsl_blas_ddot.argtypes = (gsl_vector_p, gsl_vector_p, c_double_p)
native.gsl_blas_ddot.restype = c_int
native.gsl_blas_zdotu.argtypes = (gsl_vector_complex_p, gsl_vector_complex_p,
                                  gsl_complex_p)
native.gsl_blas_zdotu.restype = c_int

native.gsl_blas_dnrm2.argtypes = (gsl_vector_p,)
native.gsl_blas_dnrm2.restype = c_double
native.gsl_blas_dznrm2.argtypes = (gsl_vector_complex_p,)
native.gsl_blas_dznrm2.restype = c_double

# Pythonic class wrapping vector functionality.
class Vector(Sequence):
    """A vector, or one-dimensional matrix of scalar values."""
    def __init__(self, *args, typecode=None):
        """Construct a new vector.

        Positional arguments:
            One positional argument is required. If this is an iterable
            object that has a length, the vector is initialised from its
            length and elements. Otherwise, it must be a positive
            integer giving the length of the new vector.

        Keyword arguments:
            typecode -- 'd' for a vector of real numbers (actually
                double-precision floating point), or 'C' for a vector of
                complex numbers (using double-precision floating point
                for the real and imaginary parts). If omitted, and the
                positional argument is an iterable, the typecode is 'd'
                if all elements of the iterable are real, and 'C'
                otherwise. If the typecode is omitted and the positional
                argument is a size, the default typecode is 'd'.

        """
        if len(args) != 1:
            raise TypeError('__init__() takes exactly 1 argument ({} '
                            'given)'.format(len(args)))

        # Determine what the positional argument is meant to be for.
        size_or_iterable = args[0]
        if isinstance(size_or_iterable, Iterable):
            init_vals = list(size_or_iterable)
            size = len(init_vals)
        else:
            init_vals = None
            size = size_or_iterable

        # Determine the appropriate typecode, if not provided.
        if typecode is None:
            if init_vals is None:
                # Default to 'd' in the absence of other information.
                typecode = 'd'
            else:
                # Use 'd' if all values are real, 'C' otherwise.
                typecode = ('d' if all(isinstance(x, Real) for x in init_vals)
                            else 'C')

        # Use the typecode argument to pick the appropriate native functions.
        native_fns = {'d': (native.gsl_vector_alloc,
                            native.gsl_vector_calloc,
                            native.gsl_vector_free,
                            native.gsl_vector_get,
                            native.gsl_vector_set,
                            native.gsl_vector_memcpy,
                            native.gsl_vector_add,
                            native.gsl_blas_ddot,
                            native.gsl_blas_dnrm2),
                      'C': (native.gsl_vector_complex_alloc,
                            native.gsl_vector_complex_calloc,
                            native.gsl_vector_complex_free,
                            native.gsl_vector_complex_get,
                            native.gsl_vector_complex_set,
                            native.gsl_vector_complex_memcpy,
                            native.gsl_vector_complex_add,
                            native.gsl_blas_zdotu,
                            native.gsl_blas_dznrm2)
                           }.get(typecode)
        if (native_fns is None):
            raise ValueError('unknown type code {!r}'.format(typecode))

        (self._alloc_fn, self._calloc_fn, self._free_fn, self._getter_fn,
         self._setter_fn, self._copy_fn, self._add_fn, self._dot_fn,
         self._norm_fn) = native_fns

        # Remember the typecode for later, so we know whether we need to call
        # other functions before or after native calls (which is needed when
        # it's a complex type, to convert Python complex to/from gsl_complex).
        self._typecode = typecode

        if init_vals is not None:
            # Don't bother initialising the block, because we're just going to
            # overwrite it in a moment anyway.
            self._alloc(size, init=False)

            for i in range(size):
                self[i] = init_vals[i]
        else:
            # Initialise the block to all zeroes.
            self._alloc(size, init=True)

        finalize.track_for_finalization(self, self._v_p, self._free_fn)

    @property
    def _as_parameter_(self):
        return self._v_p

    def _as_typecode(self, typecode):
        """Return a copy of this vector with a more general typecode.

        Vectors of real values can always be coerced to complex vectors
        with the same data type.

        """
        # Coercion rules: d coerces to C.
        if typecode == 'C' and self._typecode == 'd':
            coerced = Vector(len(self), typecode=typecode)
            for i, val in enumerate(self):
                coerced[i] = val
            return coerced
        else:
            return self

    def __getitem__(self, index):
        # FIXME: Bounds checking is not working, so I've done my own.
        # How is GSL supposed to report an out-of-bounds error to me?
        # (Crash-on-error is turned off, and turning it on still won't report
        # the problem to Python). Hence, this never raises an IndexError, and
        # the default __iter__ implementation for a Sequence never terminates.
        if not (0 <= index < len(self)):
            raise IndexError('index out of range')
        val = self._getter_fn(self._v_p, index)

        return complex(val) if self._typecode == 'C' else val

    def __setitem__(self, index, val):
        if self._typecode == 'C':
            val = gsl_complex.from_complex(val)
        self._setter_fn(self._v_p, index, val)

    def __len__(self):
        return self._v_p.contents.size

    def __copy__(self):
        """Create a shallow copy of this vector."""
        other = self.__class__(len(self), typecode=self._typecode)

        # Call the copy function and check for errors.
        errcode = self._copy_fn(other, self._v_p)
        if errcode:
            raise exception_from_result(errcode)
        else:
            return other

    def __abs__(self):
        """Find the Euclidean norm of this vector."""
        return self._norm_fn(self._v_p)

    def __add__(self, other):
        """Find the sum of this vector with another."""
        result = self.__copy__()
        # Call the native function and check for errors.
        try:
            errcode = result._add_fn(result, other)
        except ArgumentError:
            # Coerce both vectors to the more general typecode.
            result, other = (result._as_typecode(other._typecode),
                             other._as_typecode(result._typecode))
            errcode = result._add_fn(result, other)

        if errcode:
            raise exception_from_result(errcode)
        else:
            return result

    def __iadd__(self, other):
        """Add another vector to this one, in place."""
        # Call the native function (which overwrites this vector by default),
        # and check for errors.
        try:
            errcode = self._add_fn(self._v_p, other)
        except ArgumentError:
            # Create a new Vector object to hold the result of the addition.
            self = self.__copy__()
            # Coerce both vectors to the more general typecode.
            self, other = (self._as_typecode(other._typecode),
                           other._as_typecode(self._typecode))
            # Perform the addition.
            errcode = self._add_fn(self, other)

        if errcode:
            raise exception_from_result(errcode)
        else:
            return self

    def __matmul__(self, other):
        """Use the matrix multiplication operator for the dot product."""
        return self.dot(other)

    def _alloc(self, size, init):
        """Allocate a new memory block for this vector."""
        # Use calloc if we need to initialise the new block, alloc otherwise.
        vector_p = (self._calloc_fn if init else self._alloc_fn)(size)
        if not vector_p:
            # Null pointer returned; insufficient memory is available.
            raise exception_from_result(NO_MEMORY)
        else:
            self._v_p = vector_p

    def dot(self, other):
        """Calculate the scalar (dot) product of two vectors."""
        # Construct and initialise a pointer to hold the result.
        if self._typecode != other._typecode:
            self, other = (self._as_typecode(other._typecode),
                           other._as_typecode(self._typecode))

        result = pointer(gsl_complex.from_complex(0+0j)
                         if self._typecode == 'C' else
                         c_double(0.0))

        # Call the function and check for errors.
        errcode = self._dot_fn(self._v_p, other, result)
        if errcode:
            raise exception_from_result(errcode)
        else:
            return (complex(result.contents) if self._typecode == 'C' else
                    result.contents.value)
