#!/usr/bin/env python3

"""Low-level memory block functions for python-gsl."""

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

__all__ = ['gsl_block_p', 'alloc', 'free']

# Standard library imports.
from ctypes import Structure, c_double, c_size_t, POINTER

# Local imports.
from . import native
from .errors import exception_from_result

# GSL_ENOMEM error code.
NO_MEMORY = 8

# Native struct definition.
class Block(Structure):
    _fields_ = [('size', c_size_t),
                ('data', POINTER(c_double))]

gsl_block_p = POINTER(Block)

# Native function declarations.
native.gsl_block_alloc.argtypes = (c_size_t,)
native.gsl_block_alloc.restype = gsl_block_p

native.gsl_block_calloc.argtypes = (c_size_t,)
native.gsl_block_calloc.restype = gsl_block_p

def alloc(size, init=False):
    """Allocate a new block of memory."""
    # Use calloc to initialise the new block, or alloc otherwise.
    alloc_fn = native.gsl_block_calloc if init else native.gsl_block_alloc
    block_p = alloc_fn(size)
    if not block_p:
        # Null pointer returned; insufficient memory is available.
        raise exception_from_result(NO_MEMORY)
    else:
        return block_p


native.gsl_block_free.argtypes = (gsl_block_p,)

def free(block_p):
    """Free an allocated block of memory."""
    native.gsl_block_free(block_p)
