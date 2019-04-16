#!/usr/bin/env python3

"""Utility functions for python-gsl tests."""

# Copyright © 2019 Timothy Pederick.
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
import csv
from decimal import getcontext, Decimal
from pathlib import Path
import struct
import unittest

# Define precisions here to avoid an import from gsl.
DOUBLE, SINGLE, APPROX = 0, 1, 2
DEFAULT = DOUBLE

# Utility functions for manipulating floating-point representations.
STRUCT_CODES = {DOUBLE: ('!d', '!Q'),
                SINGLE: ('!f', '!L'),
                APPROX: ('!e', '!H')}

def int_from_float(f, precision):
    float_code, int_code = STRUCT_CODES[precision]
    return struct.unpack(int_code, struct.pack(float_code, f))[0]

def float_from_int(i, precision):
    float_code, int_code = STRUCT_CODES[precision]
    return struct.unpack(float_code, struct.pack(int_code, i))[0]

def bounds(n):
    bounds_dict = {}
    for precision in (DOUBLE, SINGLE, APPROX):
        n_as_int = int_from_float(n, precision)

        # At half precision, some values may be too small to distinguish from
        # zero, so subtracting 1 would cause integer underflow. The smallest
        # negative half-precision float maps to the unsigned short 32769.
        if n_as_int == 0:
            low_as_int = 32769
            high_as_int = n_as_int + 1
        else:
            low_as_int, high_as_int = n_as_int - 1, n_as_int + 1
        low, high = (float_from_int(low_as_int, precision),
                     float_from_int(high_as_int, precision))
        bounds_dict[precision] = (low, float(n), high)
    return bounds_dict

# Utility function for reading in test cases.

# The test files use 32 decimal digits, far more than enough for double
# precision.
getcontext().prec = 32

def readtests(filename):
    tests = []
    filepath = Path(__file__).parent / filename
    with filepath.open() as f:
        csv_reader = csv.reader(f)
        # Skip header row.
        next(csv_reader)

        for (in_val, *out_vals) in csv_reader:
            # The first value is the input and stays as-is. Later values are
            # output and need to be converted to bounds.
            test_case = [float(in_val)]
            test_case.extend(bounds(Decimal(val)) for val in out_vals)

            tests.append(test_case)
    return tests
