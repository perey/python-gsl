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
import copy
from ctypes import ArgumentError
from math import sqrt
import unittest

# Library to be tested.
from gsl import vector

# Data types supported.
typecodes = {'d': (float, 0.0),
             'C': (complex, 0+0j)}

# Test cases.
class TestVectorMemory(unittest.TestCase):
    """Test the low-level vector memory functions in python-gsl."""
    VECTOR_SIZE = 10
    def test_init_signature(self):
        """Test that miscalling the constructor generates an error."""
        # Does it require exactly one positional argument?
        with self.assertRaises(TypeError):
            v = vector.Vector()

        with self.assertRaises(TypeError):
            v = vector.Vector('Too many', 'arguments')

        # Does it reject a positional argument that is neither a sized iterable
        # nor a positive integer?
        with self.assertRaises(ArgumentError):
            v = vector.Vector(3.5)
        with self.assertRaises(MemoryError):
            # FIXME: This isn't really a MemoryError, but more detailed error
            # messages aren't being passed from GSL to Python... yet.
            v = vector.Vector(-1)
        with self.assertRaises(ArgumentError):
            # A generator may be iterable, but it lacks a len().
            v = vector.Vector((x for x in range(4)))

        # Does it reject an unknown typecode?
        with self.assertRaises(ValueError):
            v = vector.Vector(5, typecode='This is not a valid type code.')

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

    def test_init_from_iterable(self):
        """Test creation and initialisation of a vector."""
        values = (-1.0, 3.0, 0.0)

        # Can we create and initialise a vector of the default type (double)?
        v = vector.Vector(values)

        # Is it the right size?
        self.assertEqual(len(v), len(values))

        # Is it iterable, and are the elements the right type and value?
        for expected, got in zip(values, v):
            self.assertIsInstance(got, float)
            self.assertEqual(expected, got)


class TestVectorOperations(unittest.TestCase):
    """Test vector operations using the Python class provided."""
    def setUp(self):
        """Prepare two vectors for use in tests."""
        # Two real-valued vectors...
        self.u = vector.Vector((3.0, 0.0, -1.0))
        self.v = vector.Vector((-1.0, 1.0, 0.5))

        # ...and two complex-valued vectors.
        self.w = vector.Vector((2+1j, -2+1j, 1-2j), typecode='C')
        self.x = vector.Vector((0-1j, -1+0j, 0+0j), typecode='C')

        # Plus two differently-sized vectors, for testing size constraints.
        self.y = vector.Vector((2.5, 0.5, -1.0, 1.0))
        self.z = vector.Vector((-0.5j, 1-2j), typecode='C')

    def test_abs(self):
        """Test the absolute value (Euclidean norm) of a vector."""
        self.assertAlmostEqual(abs(self.u), sqrt(10))
        self.assertAlmostEqual(abs(self.v), sqrt(2.25))
        self.assertAlmostEqual(abs(self.w), sqrt(15))
        self.assertAlmostEqual(abs(self.x), sqrt(2))

    def test_copy(self):
        """Test shallow copying of a vector."""
        u2 = copy.copy(self.u)
        self.assertEqual(len(self.u), len(u2))
        for original, copied in zip(self.u, u2):
            self.assertEqual(original, copied)

        w2 = copy.copy(self.w)
        self.assertEqual(len(self.w), len(w2))
        for original, copied in zip(self.w, w2):
            self.assertEqual(original, copied)

    def test_dot_method_real(self):
        """Test the dot() method of two real vectors."""
        self.assertEqual(self.u.dot(self.v), -3.5)
        self.assertEqual(self.v.dot(self.u), -3.5)
        self.assertEqual(self.u.dot(self.u), 10.0)
        self.assertEqual(self.v.dot(self.v), 2.25)

    def test_dot_operator_real(self):
        """Test the @ operator with two real vectors."""
        self.assertEqual(self.u @ self.v, -3.5)
        self.assertEqual(self.v @ self.u, -3.5)
        self.assertEqual(self.u @ self.u, 10.0)
        self.assertEqual(self.v @ self.v, 2.25)

    def test_dot_mismatch_real(self):
        """Test the dot product of mixed-size real vectors."""
        with self.assertRaises(TypeError):
            self.u.dot(self.y)
        with self.assertRaises(TypeError):
            self.y.dot(self.u)
        with self.assertRaises(TypeError):
            self.u @ self.y
        with self.assertRaises(TypeError):
            self.y @ self.u

    def test_dot_method_complex(self):
        """Test the dot() method of two complex vectors."""
        self.assertEqual(self.w.dot(self.x), 3-3j)
        self.assertEqual(self.x.dot(self.w), 3-3j)
        self.assertEqual(self.w.dot(self.w), 3-4j)
        self.assertEqual(self.x.dot(self.x), 0+0j)

    def test_dot_operator_complex(self):
        """Test the @ operator with two complex vectors."""
        self.assertEqual(self.w @ self.x, 3-3j)
        self.assertEqual(self.x @ self.w, 3-3j)
        self.assertEqual(self.w @ self.w, 3-4j)
        self.assertEqual(self.x @ self.x, 0+0j)

    def test_dot_mismatch_complex(self):
        """Test the dot product of mixed-size complex vectors."""
        with self.assertRaises(TypeError):
            self.w.dot(self.z)
        with self.assertRaises(TypeError):
            self.z.dot(self.w)
        with self.assertRaises(TypeError):
            self.w @ self.z
        with self.assertRaises(TypeError):
            self.z @ self.w

    def test_dot_method_mixed(self):
        """Test the dot() method of vectors of mixed types."""
        self.assertEqual(self.u.dot(self.w), 5+5j)
        self.assertEqual(self.w.dot(self.u), 5+5j)
        self.assertEqual(self.v.dot(self.x), -1+1j)
        self.assertEqual(self.x.dot(self.v), -1+1j)

    def test_dot_operator_mixed(self):
        """Test the @ operator with vectors of mixed types."""
        self.assertEqual(self.u @ self.w, 5+5j)
        self.assertEqual(self.w @ self.u, 5+5j)
        self.assertEqual(self.v @ self.x, -1+1j)
        self.assertEqual(self.x @ self.v, -1+1j)

    def test_dot_mismatch_mixed(self):
        """Test the dot product of mixed-type, mixed-size vectors."""
        with self.assertRaises(TypeError):
            self.u.dot(self.z)
        with self.assertRaises(TypeError):
            self.w.dot(self.y)
        with self.assertRaises(TypeError):
            self.u @ self.z
        with self.assertRaises(TypeError):
            self.w @ self.y

    def test_add_real(self):
        """Test addition of two real vectors."""
        vector_sum = self.u + self.v

        # Is the result of the right type?
        self.assertIsInstance(vector_sum, vector.Vector)

        # Does it have the expected values?
        expect = (2.0, 1.0, -0.5)
        for expected, got in zip(expect, vector_sum):
            self.assertEqual(expected, got)

    def test_add_complex(self):
        """Test addition of two complex vectors."""
        vector_sum = self.w + self.x

        # Is the result of the right type?
        self.assertIsInstance(vector_sum, vector.Vector)

        # Does it have the expected values?
        expect = (2+0j, -3+1j, 1-2j)
        for expected, got in zip(expect, vector_sum):
            self.assertEqual(expected, got)

    def test_add_mixed(self):
        """Test addition of two vectors of mixed types."""
        vector_sum = self.u + self.w

        # Is the result of the right type?
        self.assertIsInstance(vector_sum, vector.Vector)

        # Does it have the expected values?
        expect = (5+1j, -2+1j, 0-2j)
        for expected, got in zip(expect, vector_sum):
            self.assertEqual(expected, got)

    def test_add_mismatch(self):
        """Test addition of two mixed-size vectors."""
        with self.assertRaises(TypeError):
            self.u + self.y
        with self.assertRaises(TypeError):
            self.w + self.z

    def test_iadd_real(self):
        """Test in-place addition of one real vector to another."""
        self.u += self.v

        # Did we avoid accidentally overwriting the vector with something that
        # isn't a vector?
        self.assertIsInstance(self.u, vector.Vector)

        # Does it have the expected values?
        expect = (2.0, 1.0, -0.5)
        for expected, got in zip(expect, self.u):
            self.assertEqual(expected, got)

    def test_iadd_complex(self):
        """Test in-place addition of one complex vector to another."""
        self.w += self.x

        # Did we avoid accidentally overwriting the vector with something that
        # isn't a vector?
        self.assertIsInstance(self.w, vector.Vector)

        # Does it have the expected values?
        expect = (2+0j, -3+1j, 1-2j)
        for expected, got in zip(expect, self.w):
            self.assertEqual(expected, got)

    def test_iadd_mixed(self):
        """Test in-place addition with vectors of mixed types."""
        self.v += self.x

        # Did we avoid accidentally overwriting the vector with something that
        # isn't a vector?
        self.assertIsInstance(self.v, vector.Vector)

        # Has the result been coerced to the correct typecode to hold the
        # result?
        self.assertEqual(self.v._typecode, 'C')

        # Does it have the expected values?
        expect = (-1-1j, 0+0j, 0.5+0j)
        for expected, got in zip(expect, self.v):
            self.assertEqual(expected, got)

    def test_iadd_mismatch(self):
        """Test in-place addition with mixed-size vectors."""
        with self.assertRaises(TypeError):
            self.u += self.y
        with self.assertRaises(TypeError):
            self.w += self.z
