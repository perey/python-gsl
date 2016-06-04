#!/usr/bin/env python3

"""Bessel functions for python-gsl."""

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

# Standard library imports.
from ctypes import c_double, c_int

# Local imports.
from .. import native
from . import sf_result_p, make_sf_result_p, sf_error_handler

# Native function declarations.
native.gsl_sf_bessel_J0.argtypes = (c_double,)
native.gsl_sf_bessel_J0.restype = c_double

def J0(x):
    """Evaluate the zeroth-order Bessel function of the first kind."""
    return native.gsl_sf_bessel_J0(x)


native.gsl_sf_bessel_J0_e.argtypes = (c_double, sf_result_p)
native.gsl_sf_bessel_J0_e.restype = c_int
native.gsl_sf_bessel_J0_e.errcheck = sf_error_handler

def J0_e(x):
    """Evaluate the zeroth-order Bessel function of the first kind."""
    result = native.gsl_sf_bessel_J0_e(x, make_sf_result_p())
    return result.val, result.err


native.gsl_sf_bessel_J1.argtypes = (c_double,)
native.gsl_sf_bessel_J1.restype = c_double

def J1(x):
    """Evaluate the first-order Bessel function of the first kind."""
    return native.gsl_sf_bessel_J1(x)


native.gsl_sf_bessel_J1_e.argtypes = (c_double, sf_result_p)
native.gsl_sf_bessel_J1_e.restype = c_int
native.gsl_sf_bessel_J1_e.errcheck = sf_error_handler

def J1_e(x):
    """Evaluate the first-order Bessel function of the first kind."""
    result = native.gsl_sf_bessel_J1_e(x, make_sf_result_p())
    return result.val, result.err


native.gsl_sf_bessel_Jn.argtypes = (c_int, c_double)
native.gsl_sf_bessel_Jn.restype = c_double

def Jn(n, x):
    """Evaluate the nth-order Bessel function of the first kind."""
    return native.gsl_sf_bessel_Jn(n, x)


native.gsl_sf_bessel_Jn_e.argtypes = (c_int, c_double, sf_result_p)
native.gsl_sf_bessel_Jn_e.restype = c_int
native.gsl_sf_bessel_Jn_e.errcheck = sf_error_handler

def Jn_e(n, x):
    """Evaluate the nth-order Bessel function of the first kind."""
    result = native.gsl_sf_bessel_Jn_e(n, x, make_sf_result_p())
    return result.val, result.err
