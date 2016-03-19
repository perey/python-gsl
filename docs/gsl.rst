===================
The ``gsl`` package
===================

.. py:module:: gsl

The top-level package namespace primarily contains internally-used objects
for binding to the shared library. However, there is one useful enumeration
defined here.

.. py:class:: Mode(enum.IntEnum)

   This enumeration has three members, :py:obj:`Mode.double`,
   :py:obj:`Mode.single` and :py:obj:`Mode.approx`, used to specify a
   desired tradeoff between speed and precision for certain functions. The
   default (also available under the name :py:obj:`Mode.default`) is always
   :py:obj:`Mode.double`.
