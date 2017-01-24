#!/usr/bin/env python3

"""Tests for Airy functions in python-gsl."""

# Copyright © 2016, 2017 Timothy Pederick.
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

# Pre-calculated results, stored as tuples of the arguments and the correct
# result, with tolerance levels. Results are correct to 32 significant figures,
# which should be plenty; double precision is accurate to around 16 significant
# figures, give or take, and the Airy function appears to be precise to only 14
# s.f. on at least some inputs.
getcontext().prec = 32
# These test cases include all of those in GSL's own test suite (namely, the
# file test_airy.c), plus a few extra. The TOL[] tolerance multipliers are from
# the GSL test suite as well. The FUDGE_FACTOR reflects GSL's own TEST_FACTOR.
FUDGE_FACTOR = 100
TOL = [FUDGE_FACTOR * base for base in [2, 16, 256, 2048, 16384, 131072]]
Ai_results = [
    # Unscaled values (hence the False).
    (-500.0, False,
     Decimal('7.2590120104041139611670153227232e-2'), TOL[4]),
    (-50.0, False,
     Decimal('-1.6188142361232092391519946940243e-1'), TOL[0]),
    (-5.0, False,
     Decimal('3.5076100902411431978801632769674e-1'), TOL[0]),
    (-0.3000000000000094, False,
     Decimal('4.3090309528558311939752211289317e-1'), TOL[0]),
    (0.6999999999999907, False,
     Decimal('1.8916240039815193192044855343497e-1'), TOL[0]),
    (1.649999999999991, False,
     Decimal('5.8310586187208854519007748854133e-2'), TOL[0]),
    (2.54999999999999, False,
     Decimal('1.4461495132954284611259897809000e-2'), TOL[0]),
    (3.499999999999987, False,
     Decimal('2.5840987869897000206587281676413e-3'), TOL[0]),
    (5.0, False,
     Decimal('1.0834442813607441734986502503346e-4'), TOL[0]),
    (5.39999999999998, False,
     Decimal('4.2729861694118644028501437917295e-5'), TOL[0]),
    (10.0, False,
     Decimal('1.1047532552898685933550205657992e-10'), TOL[0]),
    # Scaled values (hence the True).
    (-5.0, True,
     Decimal('3.5076100902411431978801632769674e-1'), TOL[0]),
    (-0.3000000000000094, True,
     Decimal('4.3090309528558311939752211289317e-1'), TOL[0]),
    (0.6999999999999907, True,
     Decimal('2.7951256676812170729652582022223e-1'), TOL[0]),
    (1.649999999999991, True,
     Decimal('2.3954930014427412216878383646911e-1'), TOL[0]),
    (2.54999999999999, True,
     Decimal('2.1836585958993876885076461974854e-1'), TOL[0]),
    (3.499999999999987, True,
     Decimal('2.0329208081635192033032302641595e-1'), TOL[0]),
    (5.39999999999998, True,
     Decimal('1.8360500932822289225958698259612e-1'), TOL[0]),
    (10.0, True,
     Decimal('1.5812366685434615027670590801715e-1'), TOL[0])
    ]
Bi_results = [ # FIXME: Source 32-s.f. values.
    # Unscaled values (hence the False).
    (-500.0, False,
     Decimal('-0.094688570132991028'), TOL[4]),
    (-5.0, False,
     Decimal('-0.1383691349016005'), TOL[1]),
    (0.6999999999999907, False,
     Decimal('0.9733286558781599'), TOL[0]),
    (1.649999999999991, False,
     Decimal('2.196407956850028'), TOL[0]),
    (2.54999999999999, False,
     Decimal('6.973628612493443'), TOL[0]),
    (3.499999999999987, False,
     Decimal('33.05550675461069'), TOL[1]),
    (5.39999999999998, False,
     Decimal('1604.476078241272'), TOL[1]),
    # Scaled values (hence the True).
    (-5.0, True,
     Decimal('-0.1383691349016005'), TOL[1]),
    (0.6999999999999907, True,
     Decimal('0.6587080754582302'), TOL[0]),
    (1.649999999999991, True,
     Decimal('0.5346449995597539'), TOL[0]),
    (2.54999999999999, True,
     Decimal('0.461835455542297'), TOL[0]),
    (3.499999999999987, True,
     Decimal('0.4201771882353061'), TOL[1]),
    (5.39999999999998, True,
     Decimal('0.3734050675720473'), TOL[0])
    ]
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
        for x, scaled, y, tol in Ai_results:
            y_actual = airy.Ai(x, scaled=scaled)
            err_actual = abs(Decimal(y_actual) - y)
##            msg.append('Ai({:.6}) = {:.6} (error {:.6})'.format(x, y_actual,
##                                                                err_actual))
            err_msg = 'Ai({:.6}) = {:.6} ≉ {:.6}'.format(x, y_actual, y)
            self.assertFloatCloseToDecimal(y_actual, y, tol, msg=err_msg)
##        self.assertTrue(False, msg='\n'.join(msg))

    def test_Ai_modes(self):
        """Test the Airy function Ai(x) with varying precision."""
##        msg = ['']
        for x, scaled, y, tol in Ai_results:
            for precision, tol_mult in precision_options:
                y_actual = airy.Ai(x, precision, scaled=scaled)
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
        for x, scaled, y, tol in Ai_results:
            val, err = airy.Ai_e(x, scaled=scaled)
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
        for x, scaled, y, tol in Ai_results:
            for precision, tol_mult in precision_options:
                val, err = airy.Ai_e(x, precision, scaled=scaled)
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

    def test_Bi(self):
        """Test the Airy function Bi(x) with default precision."""
        for x, scaled, y, tol in Bi_results:
            y_actual = airy.Bi(x, scaled=scaled)
            err_actual = abs(Decimal(y_actual) - y)
            err_msg = 'Bi({:.6}) = {:.6} ≉ {:.6}'.format(x, y_actual, y)
            self.assertFloatCloseToDecimal(y_actual, y, tol, msg=err_msg)

    def test_Bi_modes(self):
        """Test the Airy function Bi(x) with varying precision."""
        for x, scaled, y, tol in Bi_results:
            for precision, tol_mult in precision_options:
                y_actual = airy.Bi(x, precision, scaled=scaled)
                err_actual = abs(Decimal(y_actual) - y)
                err_msg = ('Bi({:.6}) = {:.6} ≉ {:.6} at precision '
                           'level {}'.format(x, y_actual, y, precision))
                self.assertFloatCloseToDecimal(y_actual, y, tol * tol_mult,
                                               msg=err_msg)

    def test_Bi_e(self):
        """Test the Airy function Bi_e(x) with default precision."""
        for x, scaled, y, tol in Bi_results:
            val, err = airy.Bi_e(x, scaled=scaled)
            err_actual = abs(Decimal(val) - y)
            err_msg_A = 'Bi({:.6}) = {:.6} ≠ {:.6} ± {:.6}'.format(x, val, y,
                                                                   err)
            err_msg_B = 'Bi({:.6}) = {:.6} = {:.6} ± {:.6}'.format(x, val, y,
                                                                   err)
            self.assertFloatWithinErrOfDecimal(val, y, err, tol,
                                               msg_failbound=err_msg_A,
                                               msg_badbound=err_msg_B)

    def test_Bi_e_modes(self):
        """Test the Airy function Bi_e(x) with varying precision."""
        for x, scaled, y, tol in Bi_results:
            for precision, tol_mult in precision_options:
                val, err = airy.Bi_e(x, precision, scaled=scaled)
                err_actual = abs(Decimal(val) - y)
                err_msg_A = ('Bi({:.6}) = {:.6} ≠ {:.6} ± {:.6} at precision '
                             'level {}'.format(x, val, y, err, precision))
                err_msg_B = ('Bi({:.6}) = {:.6} = {:.6} ± {:.6} at precision '
                             'level {}'.format(x, val, y, err, precision))
                self.assertFloatWithinErrOfDecimal(val, y, err, tol * tol_mult,
                                               msg_failbound=err_msg_A,
                                               msg_badbound=err_msg_B)
