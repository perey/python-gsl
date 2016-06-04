#!/usr/bin/env python3

"""Airy functions for python-gsl."""

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
from .. import native, gsl_mode_t, Mode
from . import sf_result_p, make_sf_result_p, sf_error_handler

# Native function declarations.
native.gsl_sf_airy_Ai.argtypes = (c_double, gsl_mode_t)
native.gsl_sf_airy_Ai.restype = c_double

def Ai(x, precision=Mode.default):
    """Evaluate the Airy function of the first kind."""
    return native.gsl_sf_airy_Ai(x, precision)


native.gsl_sf_airy_Ai_e.argtypes = (c_double, gsl_mode_t, sf_result_p)
native.gsl_sf_airy_Ai_e.restype = c_int
native.gsl_sf_airy_Ai_e.errcheck = sf_error_handler

def Ai_e(x, precision=Mode.default):
    """Evaluate the Airy function of the first kind."""
    result = native.gsl_sf_airy_Ai_e(x, precision, make_sf_result_p())
    return result.val, result.err
