#!/usr/bin/env python3

"""Error conditions for python-gsl."""

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

__all__ = ['error_codes', 'exception_from_result']

# Standard library imports.
from ctypes import c_char_p, c_int

# Local imports.
from . import native

# Native function declarations.
native.gsl_strerror.argtypes = (c_int,)
native.gsl_strerror.restype = c_char_p

# GSL error codes are perfectly well served by built-in exceptions, and we can
# use the gsl_strerror() function to get a suitable error message.
error_codes = {1: ValueError,
               2: ValueError,
               3: ValueError,
               4: ValueError,
               5: RuntimeError,
               6: ArithmeticError,
               7: RuntimeError,
               8: MemoryError,
               9: RuntimeError,
               10: RuntimeError,
               11: RuntimeError,
               12: ZeroDivisionError,
               13: ValueError,
               14: RuntimeError,
               15: ArithmeticError,
               16: OverflowError,
               17: ArithmeticError,
               18: ArithmeticError,
               19: TypeError,
               20: TypeError,
               21: ArithmeticError,
               22: ArithmeticError,
               23: OSError,
               24: NotImplementedError,
               25: MemoryError,
               26: MemoryError,
               27: RuntimeError,
               28: RuntimeError,
               29: RuntimeError,
               30: RuntimeError,
               31: RuntimeError,
               32: EOFError}

def exception_from_result(error_code):
    """Get an exception instance suitable for a GSL error code."""
    exception_class = error_codes.get(error_code, Exception)
    error_message = native.gsl_strerror(error_code).decode()

    return exception_class(error_message)
