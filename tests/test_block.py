#!/usr/bin/env python3

"""Tests for low-level memory block functions in python-gsl."""

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
from gsl import block

# Test cases.
class TestBlock(unittest.TestCase):
    """Test the memory block functions in python-gsl."""
    BLOCK_SIZE = 10

    def test_alloc(self):
        """Test block allocation and freeing."""
        my_block_p = block.alloc(self.BLOCK_SIZE)
        my_block = my_block_p.contents

        self.assertEqual(my_block.size, self.BLOCK_SIZE)
        self.assertIsInstance(my_block, Structure)

        for i in range(self.BLOCK_SIZE):
            self.assertIsInstance(my_block.data[i], float)

        block.free(my_block_p)

    def test_calloc(self):
        """Test block allocation, initialisation, and freeing."""
        my_block_p = block.alloc(self.BLOCK_SIZE, init=True)
        my_block = my_block_p.contents

        self.assertEqual(my_block.size, self.BLOCK_SIZE)
        self.assertIsInstance(my_block, Structure)

        for i in range(self.BLOCK_SIZE):
            self.assertIsInstance(my_block.data[i], float)
            self.assertEqual(my_block.data[i], 0.0)

        block.free(my_block_p)
