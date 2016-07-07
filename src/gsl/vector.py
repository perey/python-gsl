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

__all__ = []

# Standard library imports.
from ctypes import Structure, c_double, c_int, c_size_t, POINTER

# Local imports.
from . import native
from .block import gsl_block_p
from .errors import exception_from_result

# GSL_ENOMEM error code.
NO_MEMORY = 8

# Native struct definition.
class Vector(Structure):
    _fields_ = [('size', c_size_t),
                ('stride', c_size_t),
                ('data', POINTER(c_double)),
                ('block', gsl_block_p),
                ('owner', c_int)]

gsl_vector_p = POINTER(Vector)

# Native function declarations.
native.gsl_vector_alloc.argtypes = (c_size_t,)
native.gsl_vector_alloc.restype = gsl_vector_p

native.gsl_vector_calloc.argtypes = (c_size_t,)
native.gsl_vector_calloc.restype = gsl_vector_p

def alloc(size, init=False):
    """Allocate a vector in a new memory block."""
    # Use calloc to initialise the new block, or alloc otherwise.
    alloc_fn = native.gsl_vector_calloc if init else native.gsl_vector_alloc
    vector_p = alloc_fn(size)
    if not vector_p:
        # Null pointer returned; insufficient memory is available.
        raise exception_from_result(NO_MEMORY)
    else:
        return vector_p


native.gsl_vector_free.argtypes = (gsl_vector_p,)

def free(vector_p):
    """Free the memory allocated to a vector."""
    native.gsl_vector_free(vector_p)
