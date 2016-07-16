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
typecodes = {'d': (float, float, 0.0),
             'C': (gsl_complex, complex, 0+0j)}

# Test cases.
class TestVectorMemory(unittest.TestCase):
    """Test the low-level vector memory functions in python-gsl."""
    VECTOR_SIZE = 10

    def test_alloc(self):
        """Test allocating and freeing vectors."""
        v_p = vector.alloc(self.VECTOR_SIZE)
        v = v_p.contents

        self.assertEqual(v.size, self.VECTOR_SIZE)
        self.assertIsInstance(v, Structure)

        for i in range(self.VECTOR_SIZE):
            self.assertIsInstance(v.data[i], float)

        vector.free(v_p)

    def test_calloc(self):
        """Test allocating, initialising and freeing vectors."""
        v_p = vector.alloc(self.VECTOR_SIZE, init=True)
        v = v_p.contents

        self.assertEqual(v.size, self.VECTOR_SIZE)
        self.assertIsInstance(v, Structure)

        for i in range(self.VECTOR_SIZE):
            self.assertIsInstance(v.data[i], float)
            self.assertEqual(v.data[i], 0.0)

        vector.free(v_p)

    def test_alloc_by_type(self):
        """Test allocating and freeing vectors by type code."""
        for typecode in typecodes:
            itemtype, _, _ = typecodes[typecode]

            v_p = vector.alloc(self.VECTOR_SIZE, typecode=typecode)
            v = v_p.contents

            self.assertEqual(v.size, self.VECTOR_SIZE)
            self.assertIsInstance(v, Structure)

            for i in range(self.VECTOR_SIZE):
                self.assertIsInstance(v.data[i], itemtype)

            vector.free(v_p, typecode=typecode)

    def test_calloc_by_type(self):
        """Test allocating, initialising and freeing vectors by type code."""
        for typecode in typecodes:
            itemtype, conversion, initval = typecodes[typecode]

            v_p = vector.alloc(self.VECTOR_SIZE, typecode=typecode)
            v = v_p.contents

            self.assertEqual(v.size, self.VECTOR_SIZE)
            self.assertIsInstance(v, Structure)

            for i in range(self.VECTOR_SIZE):
                self.assertIsInstance(v.data[i], itemtype)
                self.assertEqual(conversion(v.data[i]), initval)

            vector.free(v_p, typecode=typecode)


class TestVectorOperations(unittest.TestCase):
    """Test the vector operations in python-gsl."""
    def setUp(self):
        """Prepare two vectors for use in tests."""
        self.u_p = vector.alloc(3, init=True)
        self.u_p.contents.data[0] = 3.0
        self.u_p.contents.data[1] = 0.0
        self.u_p.contents.data[2] = -1.0

        self.v_p = vector.alloc(3, init=True)
        self.v_p.contents.data[0] = -1.0
        self.v_p.contents.data[1] = 1.0
        self.v_p.contents.data[2] = 0.5

    def test_dot(self):
        """Test the dot product of two real vectors."""
        self.assertEqual(vector.dot(self.u_p, self.v_p), -3.5)
        self.assertEqual(vector.dot(self.v_p, self.u_p), -3.5)
        self.assertEqual(vector.dot(self.u_p, self.u_p), 10.0)
        self.assertEqual(vector.dot(self.v_p, self.v_p), 2.25)


class TestVectorClass(unittest.TestCase):
    """Test vector operations using the Python class provided."""
    def test_init(self):
        """Test creation of a vector."""
        # Does vector creation require exactly one positional argument?
        with self.assertRaises(TypeError):
            v = vector.Vector()

        # Can we create a vector of doubles?
        v = vector.Vector(5)

    def test_dot(self):
        """Test the dot product of two vectors."""
        u = vector.Vector((3.0, 0.0, -1.0))
        v = vector.Vector((-1.0, 1.0, 0.5))

        # Does it work using the dot() method?
        self.assertEqual(u.dot(v), -3.5)
        self.assertEqual(v.dot(u), -3.5)
        self.assertEqual(u.dot(u), 10.0)
        self.assertEqual(v.dot(v), 2.25)

        # Does it work using the @ operator?
        self.assertEqual(u @ v, -3.5)
        self.assertEqual(v @ u, -3.5)
        self.assertEqual(u @ u, 10.0)
        self.assertEqual(v @ v, 2.25)
