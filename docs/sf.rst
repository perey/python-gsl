=================
Special functions
=================

.. py:module:: gsl.sf

This sub-package provides a large number of special functions: mathematical
functions with established names and definitions. The standard reference for
special functions is Abramowitz and Stegun's *Handbook of Mathematical
Functions* [AS1964]_.

Most special functions can be called in two ways: a "natural" version that
simply returns the result, and an error-handling version that provides an error
bound on the result given and can flag various errors. Error-handling versions
return a 2-tuple containing the result of the calculation and the error bound.

Some functions also accept an optional ``precision`` argument. This takes a
value from :py:obj:`gsl.Mode` specifying the level of precision.

.. toctree::
   :maxdepth: 2

   airy
   bessel

References
==========

.. [AS1964] Abramowitz, M., & Stegun, I. A. (Eds.). (1964).
   |Handbook of Mathematical Functions|__ (10th printing with corrections,
   1972). Washington, D.C.: National Bureau of Standards.

   .. |Handbook of Mathematical Functions| replace:: *Handbook of Mathematical
      Functions with Formulas, Graphs, and Mathematical Tables*

   __ http://people.math.sfu.ca/~cbm/aands/intro.htm
