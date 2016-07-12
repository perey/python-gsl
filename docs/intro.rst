==========================
Introduction to python-gsl
==========================

Python-gsl is a Python 3 binding, written using the ctypes_ module from the
Python standard library, for the `GNU Scientific Library`_ ("GSL"). It offers a
wide range of mathematical and scientific functions. It is comparable to the
popular numpy_ and scipy_ packages, but python-gsl is intended to be a more
lightweight, easier-to-install alternative to these.

What's missing?
===============

The GSL_ covers a very large range of functionality, some of which is already
present in the Python standard library. As such, not everything is provided with
a Python binding.

------------------------------------------
Mathematical functions and complex numbers
------------------------------------------

In order to ease porting, GSL_ provides its own implementation of standard C
mathematical functions and constants. Since Python already provides a binding
to these in the standard library's `math`_, these are not exposed by
python-gsl. Likewise, the complex number facilities in GSL are not exposed; use
cmath_ instead. (However, the GSL *representation* of complex numbers is
provided; see :py:obj:`gsl_complex`.)

However, as at least some of the GSL_ versions of these functions make certain
accuracy guarantees, it may be the case that bindings are provided in a future
version of python-gsl.

.. _cmath: https://docs.python.org/3/library/cmath.html

.. _ctypes: https://docs.python.org/3/library/ctypes.html

.. _`GNU Scientific Library`: https://www.gnu.org/software/gsl/

.. _GSL: `GNU Scientific Library`_

.. _math: https://docs.python.org/3/library/math.html

.. _numpy: http://www.numpy.org/

.. _scipy: https://www.scipy.org/
