#!/usr/bin/env python3

"""Tests for Airy functions in python-gsl."""

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
from sys import float_info
import unittest

# Library to be tested.
from gsl.sf import airy

# Pre-calculated results, stored as 2-tuples of the argument and the correct
# result. Results are correct to 32 significant figures, which should be
# plenty; double precision is accurate to around 16 significant figures, give
# or take, and the Airy function appears to be precise to only 14 s.f. on at
# least some inputs.
getcontext().prec = 32
# These test cases include all of those in GSL's own test suite (namely, the
# file test_airy.c), plus a few extra. The TOL[] tolerance multipliers are from
# the GSL test suite as well. The FUDGE_FACTOR reflects GSL's own TEST_FACTOR.
FUDGE_FACTOR = 100
TOL = [FUDGE_FACTOR * base for base in [2, 16, 256, 2048, 16384, 131072]]
Ai_results = [(-500.0,
               Decimal('7.2590120104041139611670153227232e-2'), TOL[4]),
              (-50.0,
               Decimal('-1.6188142361232092391519946940243e-1'), TOL[0]),
              (-5.0,
               Decimal('3.5076100902411431978801632769674e-1'), TOL[0]),
              (-0.3000000000000094,
               Decimal('4.3090309528558311939752211289317e-1'), TOL[0]),
              (0.6999999999999907,
               Decimal('1.8916240039815193192044855343497e-1'), TOL[0]),
              (1.649999999999991,
               Decimal('5.8310586187208854519007748854133e-2'), TOL[0]),
              (2.54999999999999,
               Decimal('1.4461495132954284611259897809000e-2'), TOL[0]),
              (3.499999999999987,
               Decimal('2.5840987869897000206587281676413e-3'), TOL[0]),
              (5.0,
               Decimal('1.0834442813607441734986502503346e-4'), TOL[0]),
              (5.39999999999998,
               Decimal('4.2729861694118644028501437917295e-5'), TOL[0]),
              (10.0,
               Decimal('1.1047532552898685933550205657992e-10'), TOL[0])]
precision_options = ((0, 1),             # Double
                     (1, 5 * 10 ** 8),   # Single
                     (2, 25 * 10 ** 11)) # Approximate

# Test cases.
class TestAiry(unittest.TestCase):
    """Test the Airy functions in python-gsl."""
    def assertFloatCloseToDecimal(self, f, d, tol, msg=None):
        """Check float and Decimal equality to suitable precision."""
        d_f = Decimal(f)
        acceptable = (0 if d_f == d == 0 else
                      abs((d_f - d) / (d_f + d))) * tol

        self.assertAlmostEqual(d_f, d, delta=acceptable, msg=msg)

    def assertFloatWithinErrOfDecimal(self, f, d, err, tol, msg_failbound=None,
                                      msg_badbound=None):
        """Check float and Decimal equality and error margin."""
        d_f = Decimal(f)
        acceptable = (0 if d_f == d == 0 else
                      abs((d_f - d) / (d_f + d))) * tol

        self.assertAlmostEqual(d_f, d, delta=err, msg=msg_failbound)
        self.assertLess(err, acceptable, msg=msg_badbound)

    def test_Ai(self):
        """Test the Airy function Ai(x) with default precision."""
##        msg = ['']
        for x, y, tol in Ai_results:
            y_actual = airy.Ai(x)
            err_actual = abs(Decimal(y_actual) - y)
##            msg.append('Ai({:.6}) = {:.6} (error {:.6})'.format(x, y_actual,
##                                                                err_actual))
            err_msg = 'Ai({:.6}) = {:.6} ≉ {:.6}'.format(x, y_actual, y)
            self.assertFloatCloseToDecimal(y_actual, y, tol, msg=err_msg)
##        self.assertTrue(False, msg='\n'.join(msg))

    def test_Ai_modes(self):
        """Test the Airy function Ai(x) with varying precision."""
##        msg = ['']
        for x, y, tol in Ai_results:
            for precision, tol_mult in precision_options:
                y_actual = airy.Ai(x, precision)
                err_actual = abs(Decimal(y_actual) - y)
##                msg.append('Ai({:.6}, {}) = {:.6} (error '
##                           '{:.6})'.format(x, precision, y_actual, err_actual))
                err_msg = ('Ai({:.6}) = {:.6} ≉ {:.6} at precision '
                           'level {}'.format(x, y_actual, y, precision))
                self.assertFloatCloseToDecimal(y_actual, y, tol * tol_mult,
                                               msg=err_msg)
##        self.assertTrue(False, msg='\n'.join(msg))

    def test_Ai_e(self):
        """Test the Airy function Ai_e(x) with default precision."""
##        msg = ['']
        for x, y, tol in Ai_results:
            val, err = airy.Ai_e(x)
            err_actual = abs(Decimal(val) - y)
##            msg.append('Ai({:.6}) = {:.6} (error {:.6}, '
##                       'claimed {:.6})'.format(x, val, err_actual, err))
            err_msg_A = 'Ai({:.6}) = {:.6} ≠ {:.6} ± {:.6}'.format(x, val, y,
                                                                   err)
            err_msg_B = 'Ai({:.6}) = {:.6} = {:.6} ± {:.6}'.format(x, val, y,
                                                                   err)
            self.assertFloatWithinErrOfDecimal(val, y, err, tol,
                                               msg_failbound=err_msg_A,
                                               msg_badbound=err_msg_B)
##        self.assertTrue(False, msg='\n'.join(msg))

    def test_Ai_e_modes(self):
        """Test the Airy function Ai_e(x) with varying precision."""
##        msg = ['']
        for x, y, tol in Ai_results:
            for precision, tol_mult in precision_options:
                val, err = airy.Ai_e(x, precision)
                err_actual = abs(Decimal(val) - y)
##                msg.append('Ai({:.6}, {}) = {:.6} (error {:.6}, '
##                           'claimed {:.6})'.format(x, precision, val,
##                                                   err_actual, err))
                err_msg_A = ('Ai({:.6}) = {:.6} ≠ {:.6} ± {:.6} at precision '
                             'level {}'.format(x, val, y, err, precision))
                err_msg_B = ('Ai({:.6}) = {:.6} = {:.6} ± {:.6} at precision '
                             'level {}'.format(x, val, y, err, precision))
                self.assertFloatWithinErrOfDecimal(val, y, err, tol * tol_mult,
                                               msg_failbound=err_msg_A,
                                               msg_badbound=err_msg_B)
##        self.assertTrue(False, msg='\n'.join(msg))
