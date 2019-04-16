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
import unittest

# Local utility module.
from utils import DEFAULT, readtests

# Library to be tested.
from gsl.sf import airy

# Airy function tests. These include all of those in GSL's own test suite
# (namely, the file test_airy.c), plus a few extra. GSL's "tolerance" and "test
# factor" values have been abandoned in favour of lower and upper bounds.
Ai_results = readtests('test_airy_Ai.csv')
Bi_results = readtests('test_airy_Bi.csv')

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


    def test_Bi(self):
        """Test the Airy function Bi(x) with default precision."""
        for x, y_bounds, _ in Bi_results:
            with self.subTest(x=x):
                y_actual = airy.Bi(x, scaled=False)
                default_bounds = y_bounds[DEFAULT]
                err_msg = 'Bi({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(y_actual, default_bounds, msg=err_msg)

    def test_Bi_scaled(self):
        """Test the scaled Airy function Bi(x) with default precision."""
        for x, _, y_bounds in Bi_results:
            with self.subTest(x=x):
                y_actual = airy.Bi(x, scaled=True)
                default_bounds = y_bounds[DEFAULT]
                err_msg = 'Bi({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(y_actual, default_bounds, msg=err_msg)

    def test_Bi_modes(self):
        """Test the Airy function Bi(x) with varying precision."""
        for x, y_bounds, _ in Bi_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    y_actual = airy.Bi(x, precision, scaled=False)
                    bounds = y_bounds[precision]
                    err_msg = ('Bi({:.6}) not in bounds at precision level '
                               '{}'.format(x, precision))
                    self.assertFloatInBounds(y_actual, bounds, msg=err_msg)

    def test_Bi_modes_scaled(self):
        """Test the scaled Airy function Bi(x) with varying precision."""
        for x, _, y_bounds in Bi_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    y_actual = airy.Bi(x, precision, scaled=True)
                    bounds = y_bounds[precision]
                    err_msg = ('Bi({:.6}) not in bounds at precision level '
                               '{}'.format(x, precision))
                    self.assertFloatInBounds(y_actual, bounds, msg=err_msg)

    def test_Bi_e(self):
        """Test the Airy function Bi_e(x) with default precision."""
        for x, y_bounds, _ in Bi_results:
            with self.subTest(x=x):
                val, err = airy.Bi_e(x, scaled=False)
                default_bounds = y_bounds[DEFAULT]

                err_failerr = ('Bi_e({:.6}) not within claimed error '
                               '(±{:.6})'.format(x, err))
                _, y, _ = default_bounds
                self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                err_outofbounds = 'Bi_e({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(val, default_bounds,
                                         msg=err_outofbounds)

    def test_Bi_e_scaled(self):
        """Test the scaled Airy function Bi_e(x) with default precision."""
        for x, _, y_bounds in Bi_results:
            with self.subTest(x=x):
                val, err = airy.Bi_e(x, scaled=True)
                default_bounds = y_bounds[DEFAULT]

                err_failerr = ('Bi_e({:.6}) not within claimed error '
                               '(±{:.6})'.format(x, err))
                _, y, _ = default_bounds
                self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                err_outofbounds = 'Bi_e({:.6}) not in bounds'.format(x)
                self.assertFloatInBounds(val, default_bounds,
                                         msg=err_outofbounds)

    def test_Bi_e_modes(self):
        """Test the Airy function Bi_e(x) with varying precision."""
        for x, y_bounds, _ in Bi_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    val, err = airy.Bi_e(x, precision, scaled=False)
                    bounds = y_bounds[precision]

                    err_failerr = ('Bi_e({:.6}) not within claimed error '
                                   '(±{:.6}) at precision level '
                                   '{}'.format(x, err, precision))
                    _, y, _ = bounds
                    self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                    err_outofbounds = ('Bi_e({:.6}) not in bounds at precision'
                                       ' level {}'.format(x, precision))
                    self.assertFloatInBounds(val, bounds, msg=err_outofbounds)

    def test_Bi_e_modes_scaled(self):
        """Test the scaled Airy function Bi_e(x) with varying precision."""
        for x, _, y_bounds in Bi_results:
            for precision in y_bounds:
                with self.subTest(x=x, precision=precision):
                    val, err = airy.Bi_e(x, precision, scaled=True)
                    bounds = y_bounds[precision]

                    err_failerr = ('Bi_e({:.6}) not within claimed error '
                                   '(±{:.6}) at precision level '
                                   '{}'.format(x, err, precision))
                    _, y, _ = bounds
                    self.assertAlmostEqual(val, y, delta=err, msg=err_failerr)

                    err_outofbounds = ('Bi_e({:.6}) not in bounds at precision'
                                       ' level {}'.format(x, precision))
                    self.assertFloatInBounds(val, bounds, msg=err_outofbounds)
