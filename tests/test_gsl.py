#!/usr/bin/env python3

"""Tests for package-level objects in python-gsl."""

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
import unittest

# Library to be tested.
import gsl

# Test cases.
class TestComplex(unittest.TestCase):
    """Test the complex number handling in python-gsl."""
    def test_tonative(self):
        """Test conversion from Python complex numbers to C."""
        a = gsl.gsl_complex((3.0, 0.5))
        b = gsl.gsl_complex.from_complex(3.0 + 0.5j)
        self.assertEqual(a, b)

    def test_fromnative(self):
        """Test conversion from the GSL complex type to Python."""
        a = gsl.gsl_complex((3.0, 0.5))
        b = 3.0 + 0.5j
        self.assertEqual(complex(a), b)
