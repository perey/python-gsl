#!/usr/bin/env python3

"""Special functions for python-gsl."""

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

__all__ = ['sf_result', 'sf_error_handler',
           'airy', 'bessel']

# Standard library imports.
from ctypes import c_double, pointer, POINTER, Structure

# Local imports.
from ..errors import exception_from_result

# Error handling using result codes and the gsl_sf_result struct.
class sf_result(Structure):
    _fields_ = [('val', c_double),
                ('err', c_double)]


sf_result_p = POINTER(sf_result)


def make_sf_result_p():
    """Construct and initialise a pointer to a gsl_sf_result struct."""
    return pointer(sf_result(0.0, 0.0))


def sf_error_handler(result, func, arguments):
    """Check the return code and unpack the results."""
    if result:
        raise exception_from_result(result)
    else:
        # A pointer to the gsl_sf_result struct is always the last argument.
        return arguments[-1].contents
