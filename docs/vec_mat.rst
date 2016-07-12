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

.. py:function:: alloc(size, init=False)

   Allocate a new block of memory. If the optional ``alloc`` argument is
   :py:obj:`True`, the contents of the memory block are zeroed out.

   The return value of this function is a ctypes_ pointer to the new block. The
   block itself (an instance of :py:obj:`gsl.block.Block`) can be accessed as
   the ``contents`` attribute of the pointer.

.. py:function:: free(block_p)

   De-allocate the block of memory referenced by the given ctypes_ pointer.

.. _ctypes: https://docs.python.org/3/library/ctypes.html
