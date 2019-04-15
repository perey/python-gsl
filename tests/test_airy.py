#!/usr/bin/env python3

"""Tests for Airy functions in python-gsl."""

# Copyright © 2016, 2017, 2019 Timothy Pederick.
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

# Library to be tested.
from gsl.sf import airy

# Define precisions here to avoid an extra import from gsl.
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
        low_as_int, high_as_int = n_as_int - 1, n_as_int + 1
        low, high = (float_from_int(low_as_int, precision),
                     float_from_int(high_as_int, precision))
        bounds_dict[precision] = (low, float(n), high)
    return bounds_dict

# The test files use 32 decimal digits, far more than enough for double
# precision.
getcontext().prec = 32

# Read in test cases. These test cases include all of those in GSL's own test
# suite (namely, the file test_airy.c), plus a few extra. GSL's "tolerance" and
# "test factor" values have been abandoned in favour of lower and upper bounds.
Ai_results = []
Ai_file = Path(__file__).parent / 'test_airy_Ai.csv'
with Ai_file.open() as Ai:
    csv_reader = csv.reader(Ai)
    # Skip header row.
    next(csv_reader)
    for (x, y_unscaled, y_scaled) in csv_reader:
        xval = float(x)
        yval_unscaled = Decimal(y_unscaled)
        yval_scaled = Decimal(y_scaled)

        # Convert expected values to their IEEE 754 binary representations at
        # double, single, and half precisions. Add/subtract 1 (changing the
        # least significant bit of the significand) from these to get the upper
        # and lower bounds at each precision. Then convert these back into
        # floats using the appropriate precision.
        Ai_results.append((xval, bounds(yval_unscaled), bounds(yval_scaled)))


# Test cases.
class TestAiry(unittest.TestCase):
    """Test the Airy functions in python-gsl."""
    def assertFloatInBounds(self, f, bounds, msg=None):
        """Check that a float is within bounds."""
        l, _, h = bounds
        # Swap greater/less than tests when values are negative.
        if f < 0:
            l, h = h, l
        self.assertGreaterEqual(f, l, msg=msg)
        self.assertLessEqual(f, h, msg=msg)

    def test_Ai(self):
        """Test the Airy function Ai(x) with default precision."""
        for x, y_bounds, _ in Ai_results:
            with self.subTest(x=x):
                y_actual = airy.Ai(x, scaled=False)
                default_bounds = y_bounds[DEFAULT]
                err_msg = 'Ai({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(y_actual, default_bounds, msg=err_msg)

    def test_Ai_scaled(self):
        """Test the scaled Airy function Ai(x) with default precision."""
        for x, _, y_bounds in Ai_results:
            with self.subTest(x=x):
                y_actual = airy.Ai(x, scaled=True)
                default_bounds = y_bounds[DEFAULT]
                err_msg = 'Ai({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(y_actual, default_bounds, msg=err_msg)

    def test_Ai_modes(self):
        """Test the Airy function Ai(x) with varying precision."""
        for x, y_bounds, _ in Ai_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    y_actual = airy.Ai(x, precision, scaled=False)
                    bounds = y_bounds[precision]
                    err_msg = ('Ai({:.6}) not in bounds at precision level '
                               '{}'.format(x, precision))
                    self.assertFloatInBounds(y_actual, bounds, msg=err_msg)

    def test_Ai_modes_scaled(self):
        """Test the scaled Airy function Ai(x) with varying precision."""
        for x, _, y_bounds in Ai_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    y_actual = airy.Ai(x, precision, scaled=True)
                    bounds = y_bounds[precision]
                    err_msg = ('Ai({:.6}) not in bounds at precision level '
                               '{}'.format(x, precision))
                    self.assertFloatInBounds(y_actual, bounds, msg=err_msg)

    def test_Ai_e(self):
        """Test the Airy function Ai_e(x) with default precision."""
        for x, y_bounds, _ in Ai_results:
            with self.subTest(x=x):
                val, err = airy.Ai_e(x, scaled=False)
                default_bounds = y_bounds[DEFAULT]

                err_failerr = ('Ai_e({:.6}) not within claimed error '
                               '(±{:.6})'.format(x, err))
                _, y, _ = default_bounds
                self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                err_outofbounds = 'Ai_e({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(val, default_bounds,
                                         msg=err_outofbounds)

    def test_Ai_e_scaled(self):
        """Test the scaled Airy function Ai_e(x) with default precision."""
        for x, _, y_bounds in Ai_results:
            with self.subTest(x=x):
                val, err = airy.Ai_e(x, scaled=True)
                default_bounds = y_bounds[DEFAULT]

                err_failerr = ('Ai_e({:.6}) not within claimed error '
                               '(±{:.6})'.format(x, err))
                _, y, _ = default_bounds
                self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                err_outofbounds = 'Ai_e({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(val, default_bounds,
                                         msg=err_outofbounds)

    def test_Ai_e_modes(self):
        """Test the Airy function Ai_e(x) with varying precision."""
        for x, y_bounds, _ in Ai_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    val, err = airy.Ai_e(x, precision, scaled=False)
                    bounds = y_bounds[precision]

                    err_failerr = ('Ai_e({:.6}) not within claimed error '
                                   '(±{:.6}) at precision level '
                                   '{}'.format(x, err, precision))
                    _, y, _ = bounds
                    self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                    err_outofbounds = ('Ai_e({:.6}) not in bounds at precision'
                                       ' level {}'.format(x, precision))
                    self.assertFloatInBounds(val, bounds, msg=err_outofbounds)

    def test_Ai_e_modes_scaled(self):
        """Test the scaled Airy function Ai_e(x) with varying precision."""
        for x, _, y_bounds in Ai_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    val, err = airy.Ai_e(x, precision, scaled=True)
                    bounds = y_bounds[precision]

                    err_failerr = ('Ai_e({:.6}) not within claimed error '
                                   '(±{:.6}) at precision level '
                                   '{}'.format(x, err, precision))
                    _, y, _ = bounds
                    self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                    err_outofbounds = ('Ai_e({:.6}) not in bounds at precision'
                                       ' level {}'.format(x, precision))
                    self.assertFloatInBounds(val, bounds, msg=err_outofbounds)
