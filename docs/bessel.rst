================
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
