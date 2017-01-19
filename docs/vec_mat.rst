====================
Vectors and matrices
====================

Blocks
======

.. py:module:: gsl.block

GSL allocates memory for vectors and matrices in terms of blocks. Generally, it
is not necessary to allocate or access these directly, but the functions to do
so are available from python-gsl.

.. py:class:: Block

   A ctypes_ Structure subclass.

   .. py:attribute:: size

      The number of elements in the block.

   .. py:attribute:: data

      An iterable over the elements in the block.

.. py:function:: alloc(size, typecode='d', init=False)

   Allocate a new block of memory. If the optional ``init`` argument is
   :py:obj:`True`, the contents of the memory block are zeroed out.

   The native data type stored in the block is set by the ``typecode``
   argument. Recognised values are:

   ========= ==============================================
   Type code                  Native type
   ========= ==============================================
   'C'       :py:obj:`gsl.gsl_complex` (complex)
   'd'       ``c_double`` (double-precision floating point)
   ========= ==============================================

   The return value of this function is a ctypes_ pointer to the new block. The
   block itself (an instance of :py:obj:`gsl.block.Block`) can be accessed as
   the ``contents`` attribute of the pointer.

.. py:function:: free(block_p, typecode='d')

   De-allocate the block of memory referenced by the given ctypes_ pointer.

.. _ctypes: https://docs.python.org/3/library/ctypes.html

Vectors
=======

.. py:module:: gsl.vector

.. py:class:: Vector(*args, typecode=None)

   A vector, or one-dimensional matrix of scalar values. When creating a
   :py:class:`Vector` instance, there must be one positional argument: either a
   length, or an iterable giving the initial values. The optional ``typecode``
   argument is keyword-only; if omitted, it will be inferred from the given
   initial values, or default to 'd' if a length is given. (See
   :py:func:`gsl.block.alloc` for available typecodes and their meanings.)

   The class implements the sequence_ interface, but while :py:class:`Vector`
   instances are not immutable, they only allow item assignment, not other
   operations of the mutable sequence interface (such as item deletion).

   The following operators and built-ins are defined on :py:class:`Vector`
   instances:

   * Addition (both ``+`` and ``+=``)
   * Scalar multiplication (dot product) with the ``@`` operator
   * :py:func:`!abs`, to find the magnitude (Euclidean norm, or "length" of
     the vector in Euclidean geometry)

   Operations on vectors with different typecodes will coerce the result to an
   appropriate typecode that can accommodate all values. For example, adding a
   complex vector and a real vector will result in a complex vector.

   .. py:method:: __copy__()

      Create a shallow copy of this vector. The signature of this method makes
      it compatible with the standard library's :py:func:`copy.copy` function.

   .. py:method:: dot(other)

      Calculate the scalar (dot) product of this vector and another. This
      method is also available using the ``@`` operator. (Using ``@`` for this
      and not for the cross product follows the example of `PEP 465`_, which
      introduced the operator.)

.. _sequence: https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence

.. _`PEP 465`: https://www.python.org/dev/peps/pep-0465/
