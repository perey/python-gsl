====================
Vectors and matrices
====================

Blocks
======

.. py:module:: gsl.block

GSL allocates memory for vectors and matrices in terms of blocks. Generally, it
is not necessary to allocate or access these directly, but the functions to do
so are available from python-gsl.

.. py:function:: alloc(size, init=False)

Allocate a new block of memory. If the optional ``alloc`` argument is
:py:obj:`True`, the contents of the memory block are zeroed out.
