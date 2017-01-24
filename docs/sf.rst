=================
Special functions
=================

.. py:module:: gsl.sf

Most special functions come in two kinds: a "natural" version that simply
returns the result, and an error-handling version that provides an error
bound on the result given and can flag various errors. Error-handling versions
return a 2-tuple containing the result of the calculation and the error bound.

Some functions also accept an optional ``precision`` argument. This takes a
value from :py:obj:`gsl.Mode` specifying the level of precision.

Airy functions
==============

.. py:module:: gsl.sf.airy

The Airy functions :math:`Ai(z)` and :math:`Bi(z)` are a pair of
linearly-independent solutions to the differential equation:

.. math:: w'' - z w = 0

:math:`Ai(z)` is also known as *the* Airy function, or the Airy function of the
first kind. :math:`Bi(z)` is known as the Airy function of the second kind, or
the Bairy function.

In Abramowitz and Stegun, the Airy functions are covered in section 10.4
[Antosiewicz1964]_.

Note that the GSL_ Airy functions accept only real arguments.

.. py:function:: Ai(x, precision=Mode.default, scaled=False)

.. py:function:: Ai_e(x, precision=Mode.default, scaled=False)

Evaluate :math:`Ai(x)`, the Airy function of the first kind, in natural and
error-handling versions. If the ``scaled`` argument is ``True``, a scaling
factor is applied. For :math:`x < 0`, the scaling factor is 1. For
:math:`x > 0`, over which :math:`Ai(x) \to 0`, the scaling factor is
:math:`s(x) = \exp \left( \frac{2}{3} x^\frac{3}{2} \right)`.

.. py:function:: Bi(x, precision=Mode.default)

.. py:function:: Bi_e(x, precision=Mode.default)

Evaluate :math:`Bi(x)`, the Airy function of the second kind, in natural and
error-handling versions. If the ``scaled`` argument is ``True``, a scaling
factor is applied. For :math:`x < 0`, the scaling factor is 1. For
:math:`x > 0`, over which :math:`Bi(x) \to \infty`, the scaling factor is
:math:`s(x) = \exp \left( -\frac{2}{3} x^\frac{3}{2} \right)`.

.. py:function:: Ai_deriv(x, precision=Mode.default, scaled=False)

.. py:function:: Ai_deriv_e(x, precision=Mode.default, scaled=False)

.. py:function:: Bi_deriv(x, precision=Mode.default, scaled=False)

.. py:function:: Bi_deriv_e(x, precision=Mode.default, scaled=False)

Evaluate :math:`Ai'(x)` and :math:`Bi'(x)`, the derivatives of the Airy
functions of the first and second kinds.

.. py:function:: zero_Ai(s, precision=Mode.default)

.. py:function:: zero_Ai_e(s, precision=Mode.default)

.. py:function:: zero_Ai_deriv(x, precision=Mode.default)

.. py:function:: zero_Ai_deriv_e(x, precision=Mode.default)

.. py:function:: zero_Bi(s, precision=Mode.default)

.. py:function:: zero_Bi_e(s, precision=Mode.default)

.. py:function:: zero_Bi_deriv(x, precision=Mode.default)

.. py:function:: zero_Bi_deriv_e(x, precision=Mode.default)

Locate the :math:`s`-th zeroes of the Airy functions and their derivatives.
Zeroes are located on the negative real axis, and are numbered in order as
:math:`x \to -\infty`.

Bessel functions
================

.. py:module:: gsl.sf.bessel

The Bessel functions are the solutions of the differential equation:

.. math:: z^2 \frac{d^2 w}{d z^2} + z \frac{d w}{d z} + \left(z^2 - \nu^2 \right) w = 0

The constant :math:`\nu` is called the *order* of the Bessel function.

In Abramowitz and Stegun, the Bessel functions are covered in chapters 9
[Olver1964]_ and 10 [Antosiewicz1964]_.

References
==========

.. [Antosiewicz1964] Antosiewicz, H. A. (1964).
   `Bessel functions of fractional order`_.
   In Abramowitz, M., & Stegun, I. A. (Eds.). (1964). *Handbook of Mathematical
   Functions with Formulas, Graphs, and Mathematical Tables* (10th printing
   with corrections, 1972). Washington, D.C.: National Bureau of Standards.

.. [Olver1964] Olver, F. W. J (1964).
   `Bessel functions of integer order`_.
   In Abramowitz, M., & Stegun, I. A. (Eds.). (1964). *Handbook of Mathematical
   Functions with Formulas, Graphs, and Mathematical Tables* (10th printing
   with corrections, 1972). Washington, D.C.: National Bureau of Standards.

.. _`Bessel functions of fractional order`: http://people.math.sfu.ca/~cbm/aands/page_435.htm

.. _`Bessel functions of integer order`: http://people.math.sfu.ca/~cbm/aands/page_355.htm

.. _`GNU Scientific Library`: https://www.gnu.org/software/gsl/

.. _GSL: `GNU Scientific Library`_