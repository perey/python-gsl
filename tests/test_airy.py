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

# Library to be tested.
from gsl.sf import airy

# Define precisions here to avoid an extra import from gsl.
DOUBLE, SINGLE, APPROX = 0, 1, 2
DEFAULT = DOUBLE

# These test cases include all of those in GSL's own test suite (namely, the
# file test_airy.c), plus a few extra. GSL's "tolerance" and "test factor"
# values have been abandoned in favour of lower and upper bounds.
#
# Each test case is a 3-tuple comprising an input value, a boolean stating
# whether or not the test uses scaled values, and a dict of result bounds. Keys
# in this dict are precisions, and values are 3-tuples giving a lower bound,
# an expected value, and an upper bound. To avoid loss of precision from
# decimal representation, bounds are given as hex strings that can be passed to
# float.fromhex().
Ai_results = [
    # Unscaled values.
    (-500.0, False,
     {DOUBLE: ('0x1.295441fdc0cb3p-4', '0x1.295441fdc0cb4p-4',
               '0x1.295441fdc0cb5p-4'),
      SINGLE: ('0x1.295440p-4', '0x1.295442p-4', '0x1.295444p-4'),
      APPROX: ('0x1.290p-4', '0x1.294p-4', '0x1.298p-4')}),
    (-50.0, False,
     {DOUBLE: ('-0x1.4b887ce1f56eep-3', '-0x1.4b887ce1f56efp-3',
               '-0x1.4b887ce1f56f0p-3'),
      SINGLE: ('-0x1.4b887cp-3', '-0x1.4b8880p-3'),
      APPROX: ('-0x1.4b4p-3', '-0x1.4bcp-3')}),
    (-5.0, False,
     {DOUBLE: ('0x1.672de4d9e1d31p-2', '0x1.672de4d9e1d32p-2',
               '0x1.672de4d9e1d33p-2'),
      SINGLE: ('0x1.672de2p-2', '0x1.672de4p-2', '0x1.672de6p-2'),
      APPROX: ('0x1.670p-2', '0x1.670p-2', '0x1.678p-2')}),
    (-0.3000000000000094, False,
     {DOUBLE: ('0x1.b93ea937fcac5p-2', '0x1.b93ea937fcac6p-2',
               '0x1.b93ea937fcac7p-2'),
      SINGLE: ('0x1.b93ea8p-2', '0x1.b93eaap-2', '0x1.b93eacp-2'),
      APPROX: ('0x1.b90p-2', '0x1.b94p-2', '0x1.b98p-2')}),
    (0.6999999999999907, False,
     {DOUBLE: ('0x1.8367939abe4ccp-3', '0x1.8367939abe4cdp-3',
               '0x1.8367939abe4cep-3'),
      SINGLE: ('0x1.836792p-3', '0x1.836794p-3', '0x1.836796p-3'),
      APPROX: ('0x1.834p-3', '0x1.838p-3', '0x1.83cp-3')}),
    (1.649999999999991, False,
     {DOUBLE: ('0x1.ddae2995e8a9fp-5', '0x1.ddae2995e8aa0p-5',
               '0x1.ddae2995e8aa1p-5'),
      SINGLE: ('0x1.ddae28p-5', '0x1.ddae2ap-5', '0x1.ddae2cp-5'),
      APPROX: ('0x1.dd8p-5', '0x1.ddcp-5', '0x1.de0p-5')}),
    (2.54999999999999, False,
     {DOUBLE: ('0x1.d9dfd052dac93p-7', '0x1.d9dfd052dac94p-7',
               '0x1.d9dfd052dac95p-7'),
      SINGLE: ('0x1.d9dfcep-7', '0x1.d9dfd0p-7', '0x1.d9dfd2p-7'),
      APPROX: ('0x1.d98p-7', '0x1.d9cp-7', '0x1.da0p-7')}),
    (3.499999999999987, False,
     {DOUBLE: ('0x1.52b3f78f3beb9p-9', '0x1.52b3f78f3beb9p-9',
               '0x1.52b3f78f3bebbp-9'),
      SINGLE: ('0x1.52b3f6p-9', '0x1.52b3f8p-9', '0x1.52b3fap-9'),
      APPROX: ('0x1.528p-9', '0x1.52cp-9', '0x1.530p-9')}),
    (5.0, False,
     {DOUBLE: ('0x1.c66df1a2952d4p-14', '0x1.c66df1a2952d5p-14',
               '0x1.c66df1a2952d6p-14'),
      SINGLE: ('0x1.c66df0p-14', '0x1.c66df2p-14', '0x1.c66df4p-14'),
      APPROX: ('0x1.c64p-14', '0x1.c68p-14', '0x1.c6cp-14')}),
    (5.39999999999998, False,
     {DOUBLE: ('0x1.6671ade499cdep-15', '0x1.6671ade499cdfp-15',
               '0x1.6671ade499ce0p-15'),
      SINGLE: ('0x1.6671acp-15', '0x1.6671aep-15', '0x1.6671b0p-15'),
      APPROX: ('0x1.664p-15', '0x1.668p-15', '0x1.66cp-15')}),
    (10.0, False,
     {DOUBLE: ('0x1.e5e028a1f8cd9p-34', '0x1.e5e028a1f8cdap-34',
               '0x1.e5e028a1f8cdbp-34'),
      SINGLE: ('0x1.e5e026p-34', '0x1.e5e028p-34', '0x1.e5e02ap-34'),
      APPROX: ('0x1.e5cp-34', '0x1.e60p-34', '0x1.e64p-34')}),
    # Scaled values.
    (-5.0, True,
     {DOUBLE: ('0x1.672de4d9e1d31p-2', '0x1.672de4d9e1d32p-2',
               '0x1.672de4d9e1d33p-2'),
      SINGLE: ('0x1.672de2p-2', '0x1.672de4p-2', '0x1.672de6p-2'),
      APPROX: ('0x1.670p-2', '0x1.674p-2', '0x1.678p-2')}),
    (-0.3000000000000094, True,
     {DOUBLE: ('0x1.b93ea937fcac5p-2', '0x1.b93ea937fcac6p-2',
               '0x1.b93ea937fcac7p-2'),
      SINGLE: ('0x1.b93ea7p-2', '0x1.b93eabp-2'),
      APPROX: ('0x1.b90p-2', '0x1.b98p-2')}),
    (0.6999999999999907, True,
     {DOUBLE: ('0x1.1e388ad45c42ep-2', '0x1.1e388ad45c42fp-2',
               '0x1.1e388ad45c430p-2'),
      SINGLE: ('0x1.1e388ad45c42ep-2', '0x1.1e388ad45c430p-2'),
      APPROX: ('0x1.1e388ad45c42ep-2', '0x1.1e388ad45c430p-2')}),
    (1.649999999999991, True,
     {DOUBLE: ('0x1.ea98d2cf31dbfp-3', '0x1.ea98d2cf31dc0p-3',
               '0x1.ea98d2cf31dc1p-3'),
      SINGLE: ('0x1.ea98d0p-3', '0x1.ea98d2p-3', '0x1.ea98d4p-3'),
      APPROX: ('0x1.ea4p-3', '0x1.ea8p-3', '0x1.eacp-3')}),
    (2.54999999999999, True,
     {DOUBLE: ('0x1.bf36998c03831p-3', '0x1.bf36998c03832p-3',
               '0x1.bf36998c03833p-3'),
      SINGLE: ('0x1.bf3698p-3', '0x1.bf369ap-3', '0x1.bf369cp-3'),
      APPROX: ('0x1.bf0p-3', '0x1.bf4p-3', '0x1.bf8p-3')}),
    (3.499999999999987, True,
     {DOUBLE: ('0x1.a057993522db9p-3', '0x1.a057993522dbap-3',
               '0x1.a057993522dbbp-3'),
      SINGLE: ('0x1.a05798p-3', '0x1.a0579ap-3', '0x1.a0579cp-3'),
      APPROX: ('0x1.a00p-3', '0x1.a04p-3', '0x1.a08p-3')}),
    (5.0, True,
     {DOUBLE: ('0x1.7efaf788e68ffp-3', '0x1.7efaf788e6900p-3',
               '0x1.7efaf788e6901p-3'),
      SINGLE: ('0x1.7efaf6p-3', '0x1.7efaf8p-3', '0x1.7efafap-3'),
      APPROX: ('0x1.7ecp-3', '0x1.7f0p-3', '0x1.7f4p-3')}),
    (5.39999999999998, True,
     {DOUBLE: ('0x1.7805e733926a7p-3', '0x1.7805e733926a8p-3',
               '0x1.7805e733926a9p-3'),
      SINGLE: ('0x1.7805e6p-3', '0x1.7805e8p-3', '0x1.7805eap-3'),
      APPROX: ('0x1.77cp-3', '0x1.780p-3', '0x1.784p-3')}),
    (10.0, True,
     {DOUBLE: ('0x1.43d6574ee774dp-3', '0x1.43d6574ee774ep-3',
               '0x1.43d6574ee774fp-3'),
      SINGLE: ('0x1.43d656p-3', '0x1.43d658p-3', '0x1.43d65ap-3'),
      APPROX: ('0x1.40p-3', '0x1.44p-3', '0x1.48p-3')})
    ]

# Test cases.
class TestAiry(unittest.TestCase):
    """Test the Airy functions in python-gsl."""
    def assertFloatInBounds(self, f, bounds, msg=None):
        """Check that a float is within bounds."""
        lhex, _, hhex = bounds
        l, h = (float.fromhex(bound) for bound in (lhex, hhex))
        self.assertGreaterEqual(f, l, msg=msg)
        self.assertLessEqual(f, h, msg=msg)

    def assertFloatWithinErr(self, f, expected, err, msg=None):
        """Check that a float is within an error margin."""
        self.assertAlmostEqual(f, float.fromhex(expected), delta=err,
                               msg=msg)

    def test_Ai(self):
        """Test the Airy function Ai(x) with default precision."""
        for x, scaled, y_bounds in Ai_results:
            y_actual = airy.Ai(x, scaled=scaled)
            default_bounds = y_bounds[DEFAULT]
            err_msg = 'Ai({:.6}, {}) not in bounds'.format(x, scaled)
            self.assertFloatInBounds(y_actual, default_bounds, msg=err_msg)

    def test_Ai_modes(self):
        """Test the Airy function Ai(x) with varying precision."""
        for x, scaled, y_bounds in Ai_results:
            for precision in y_bounds:
                y_actual = airy.Ai(x, precision, scaled=scaled)
                bounds = y_bounds[precision]
                err_msg = ('Ai({:.6}, {}) not in bounds at precision level '
                           '{}'.format(x, scaled, precision))
                self.assertFloatInBounds(y_actual, bounds, msg=err_msg)

    def test_Ai_e(self):
        """Test the Airy function Ai_e(x) with default precision."""
        for x, scaled, y_bounds in Ai_results:
            val, err = airy.Ai_e(x, scaled=scaled)
            default_bounds = y_bounds[DEFAULT]

            err_failerr = ('Ai_e({:.6}, {}) not within claimed error '
                           '(±{:.6})'.format(x, scaled, err))
            _, y, _ = default_bounds
            self.assertFloatWithinErr(val, y, err, msg=err_failerr)

            err_outofbounds = 'Ai_e({:.6}, {}) not in bounds'.format(x, scaled)
            self.assertFloatInBounds(val, default_bounds, msg=err_outofbounds)

    def test_Ai_e_modes(self):
        """Test the Airy function Ai_e(x) with varying precision."""
        for x, scaled, y_bounds in Ai_results:
            for precision in y_bounds:
                val, err = airy.Ai_e(x, precision, scaled=scaled)
                bounds = y_bounds[precision]

                err_failerr = ('Ai_e({:.6}, {}) not within claimed error '
                               '(±{:.6}) at precision level '
                               '{}'.format(x, scaled, err, precision))
                _, y, _ = bounds
                self.assertFloatWithinErr(val, y, err, msg=err_failerr)

                err_outofbounds = ('Ai_e({:.6}, {}) not in bounds at precision'
                                   ' level {}'.format(x, scaled, precision))
                self.assertFloatInBounds(val, bounds, msg=err_outofbounds)
