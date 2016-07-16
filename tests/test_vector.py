#!/usr/bin/env python3

"""Tests for vector operations in python-gsl."""

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
from ctypes import Structure
import unittest

# Library to be tested.
from gsl import vector

# Test dependency.
from gsl import gsl_complex

# Data types supported.
typecodes = {'d': (float, 0.0),
             'C': (complex, 0+0j)}

# Test cases.
class TestVectorMemory(unittest.TestCase):
    """Test the low-level vector memory functions in python-gsl."""
    VECTOR_SIZE = 10
    def test_init_signature(self):
        """Test that miscalling the constructor generates an error."""
        # Does vector creation require exactly one positional argument?
        with self.assertRaises(TypeError):
            v = vector.Vector()

        with self.assertRaises(TypeError):
            v = vector.Vector('Too many', 'arguments')

    def test_init(self):
        """Test creation of a vector with default arguments."""
        # Can we create a vector of the default type (double)?
        v = vector.Vector(self.VECTOR_SIZE)

        # Is it the right size?
        self.assertEqual(len(v), self.VECTOR_SIZE)

        # Is it iterable, and are the elements the right type and initialised
        # to zero?
        for x in v:
            self.assertIsInstance(x, float)
            self.assertEqual(x, 0.0)

        #FIXME: Iteration isn't working!!

    def test_init_by_type(self):
        """Test creation of a vector with a typecode."""
        for typecode in typecodes:
            itemtype, zeroval = typecodes[typecode]

            # Can we create a vector of this type?
            v = vector.Vector(self.VECTOR_SIZE, typecode=typecode)

            # Is it the right size?
            self.assertEqual(len(v), self.VECTOR_SIZE)

            # Is it iterable, and are the elements the right type and
            # initialised to zero?
            for x in v:
                self.assertIsInstance(x, itemtype)
                self.assertEqual(x, zeroval)


class TestVectorOperations(unittest.TestCase):
    """Test vector operations using the Python class provided."""
    def setUp(self):
        """Prepare two vectors for use in tests."""
        self.u = vector.Vector((3.0, 0.0, -1.0))
        self.v = vector.Vector((-1.0, 1.0, 0.5))

    def test_dot(self):
        """Test the dot product of two vectors."""
        # Does it work using the dot() method?
        self.assertEqual(self.u.dot(self.v), -3.5)
        self.assertEqual(self.v.dot(self.u), -3.5)
        self.assertEqual(self.u.dot(self.u), 10.0)
        self.assertEqual(self.v.dot(self.v), 2.25)

        # Does it work using the @ operator?
        self.assertEqual(self.u @ self.v, -3.5)
        self.assertEqual(self.v @ self.u, -3.5)
        self.assertEqual(self.u @ self.u, 10.0)
        self.assertEqual(self.v @ self.v, 2.25)
