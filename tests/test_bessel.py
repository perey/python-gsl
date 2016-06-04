#!/usr/bin/env python3

"""Tests for Bessel functions in python-gsl."""

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
from decimal import getcontext, Decimal
import unittest

# Library to be tested.
from gsl.sf import bessel

# Pre-calculated results, stored as 3-tuples: the order of the function, the
# argument to the function, and the correct result. Results are correct to 32
# significant figures, which should be plenty, as double precision is accurate
# to at least 15 significant figures.
getcontext().prec = 32
J_results = [(0, 5.0, Decimal('-0.17759677131433830434739701307476')),
             (1, 5.0, Decimal('-0.32757913759146522203773432191017'))]

# Test cases.
class TestBessel(unittest.TestCase):
    """Test the Bessel functions in python-gsl."""
    def assertFloatCloseToDecimal(self, f, d):
        """Check float and Decimal equality to suitable precision."""
        self.assertAlmostEqual(Decimal(f), d, places=15)

    def assertFloatWithinErrOfDecimal(self, f, d, err):
        """Check float and Decimal equality and error margin.."""
        d_f = Decimal(f)

        self.assertAlmostEqual(d_f, d, places=15)

        self.assertGreaterEqual(err, 0)
        self.assertLess(err, 1e-15)

        self.assertLess(abs(d_f - d), err)

    def test_J0(self):
        """Test the Bessel function J0(x)."""
        for order, x, y in J_results:
            if order == 0:
                self.assertFloatCloseToDecimal(bessel.J0(x), y)

    def test_J0_e(self):
        """Test the Bessel function J0(x) with error handling."""
        for order, x, y in J_results:
            if order == 0:
                val, err = bessel.J0_e(x)
                self.assertFloatWithinErrOfDecimal(val, y, err)

    def test_J1(self):
        """Test the Bessel function J1(x)."""
        for order, x, y in J_results:
            if order == 1:
                self.assertFloatCloseToDecimal(bessel.J1(x), y)

    def test_J1_e(self):
        """Test the Bessel function J1(x) with error handling."""
        for order, x, y in J_results:
            if order == 1:
                val, err = bessel.J1_e(x)
                self.assertFloatWithinErrOfDecimal(val, y, err)

    def test_Jn(self):
        """Test the Bessel function Jn(x)."""
        for order, x, y in J_results:
            self.assertFloatCloseToDecimal(bessel.Jn(order, x), y)

    def test_Jn_e(self):
        """Test the Bessel function Jn(x), with error handling."""
        for order, x, y in J_results:
            val, err = bessel.Jn_e(order, x)
            self.assertFloatWithinErrOfDecimal(val, y, err)
