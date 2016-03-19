#!/usr/bin/env python3

"""Tests for Airy functions in python-gsl."""

# Copyright © 2016 Timothy Pederick.
#
# Based on the GNU Scientific Library (GSL):
#     Copyright © 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
#     2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015 The GSL Team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
from decimal import getcontext, Decimal
import unittest

# Library to be tested.
from gsl.sf import airy

# Pre-calculated results, stored as 2-tuples of the argument and the correct
# result. Results are correct to 32 significant figures, which should be
# plenty; double precision is accurate to around 16 significant figures, give
# or take, and the Airy function appears to be precise to only 14 s.f. on at
# least some inputs.
getcontext().prec = 32
Ai_results = [(-5.0, Decimal('0.35076100902411431978801632769674')),
              (5.0, Decimal('0.00010834442813607441734986502503346'))]

# Test cases.
class TestAiry(unittest.TestCase):
    """Test the Airy functions in python-gsl."""
    def assertFloatCloseToDecimal(self, f, d, places=15):
        """Check float and Decimal equality to suitable precision."""
        self.assertAlmostEqual(Decimal(f), d, places=places)

    def assertFloatWithinErrOfDecimal(self, f, d, err, places=15):
        """Check float and Decimal equality and error margin."""
        d_f = Decimal(f)

        self.assertAlmostEqual(d_f, d, places=places)

        self.assertGreaterEqual(err, 0)
        self.assertLess(err, 10 ** -places)

        self.assertLess(abs(d_f - d), err)

    def test_Ai(self):
        """Test the Airy function Ai(x)."""
        for x, y in Ai_results:
            self.assertFloatCloseToDecimal(airy.Ai(x), y)

    def test_Ai_modes(self):
        """Test the Airy function Ai(x) with different precisions."""
        for x, y in Ai_results:
            for precision, places in ((0, 15), # Double
                                      (1, 7),  # Single
                                      (2, 3)): # Approximate
                self.assertFloatCloseToDecimal(airy.Ai(x, precision), y,
                                               places)

    def test_Ai_e(self):
        """Test the Airy function Ai(x) with error handling."""
        for x, y in Ai_results:
            val, err = airy.Ai_e(x)
            self.assertFloatWithinErrOfDecimal(val, y, err, places=14)

    def test_Ai_e_modes(self):
        """Test the Airy function Ai(x) with errors and precisions."""
        for x, y in Ai_results:
            for precision, places in ((0, 14), # Double
                                      (1, 7),  # Single
                                      (2, 3)): # Approximate
                val, err = airy.Ai_e(x, precision)
                self.assertFloatWithinErrOfDecimal(val, y, err, places)
