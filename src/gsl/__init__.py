#!/usr/bin/env python3

"""python-gsl: A Python 3 binding to the GNU Scientific Library."""

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

__all__ = ['native', 'gsl_complex', 'gsl_mode_t', 'Mode',
           'block', 'vector', 'errors', 'sf',
           'finalize']

# Standard library imports.
from enum import IntEnum
from ctypes import Structure, c_double, c_uint, c_void_p

# Import objects from submodules that are to be available at the package level.
from ._native import native

# Import objects from submodules that are used here.
from .errors import exception_on_error, set_error_handler

# Disable crash-on-error and raise Python exceptions instead.
set_error_handler(exception_on_error)

# Define GSL complex number formats.
class gsl_complex(Structure):
    _fields_ = [('dat', c_double * 2)]

    @classmethod
    def from_complex(cls, c):
        """Convert a Python complex number to a gsl_complex object."""
        return cls((c.real, c.imag))

    def __complex__(self):
        """Convert this gsl_complex object to a Python complex number."""
        return complex(*self.dat)

    def __eq__(self, other):
        """Compare for itemwise equality between this and another value."""
        return (isinstance(other, self.__class__) and
                all(mine == others for mine, others in zip(self.dat,
                                                           other.dat)))

# Define mode (precision) specifiers.
gsl_mode_t = c_uint
class Mode(IntEnum):
    default = 0
    double = 0
    single = 1
    approx = 2
