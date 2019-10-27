# Quantumformatics

Framework for simulating quantum information and computation theory on classic computers.

## Table of Contents

## Example

## Setup

## Dirac notation

Dirac notation is a convenient notation to represent linear algebra concepts, such as row and column vectors, matrices and linear algebra operations, in a human readable format for quick computation by hand. The purpose of Dirac notation in this repository is to increase readability and usability of the package for the users. You can describe and read quantum states in terms of kets and bras, which on computer is way simpler than trying to read multidimensional arrays.

### Design

`Matrix` class represents an arbitrary matrix in a d-dimensional Hilbert space. `Ket` and `Bra` classes are derived from `Matrix` class and represent column and row vectors respectively. Dirac notation implementation uses `numpy` package under the hood to hold the values and perform calculations. The main motivation behind having distinct `Ket` and `Bra` classes is the fact that `numpy` does not support column vectors natively (all vectors are treated as `(n,)` shape `np.ndarray`), which makes it harder to write BraKet notation using it.

### Usage

Basic objects can be created from `list` and `np.ndarray` objects, `Bra` object can also be created from `Ket` (using adjoint operation):

```python
ket_0 = Ket([1, 0])  # |0>
ket_1 = Ket([0, 1])  # |1>

bra_0 = Bra([1, 0]) = Bra(ket_0)  # <0|, created from |0>
bra_1 = Bra([0, 1]) = Bra(ket_1)  # <1|, created from |1>

identity = Matrix(np.array([[1,0], [0, 1]]))  # I = [ 1 0 / 0 1 ]
```

You can use arithmetic and comparison operators on these objects and therefore construct new objects:

```python
ket_x = ket_0 + ket_1  # |0> + |1>
ket_y = 2 * ket_x  # 2|0> + 2|1>
product = bra_0 * ket_0  # 1
```

You can also construct `Matrix` using `Bra` and `Ket`:

```python
matrix = ket_0 * bra_0  # |0><0| = [ 1 0 / 0 0 ]
```

You can either use the operators to perform mathematical functions, or you can use functions provided in the `functions.py` file.

```python
from src.dirac_notation import functions as dirac

dirac.add(ket_0, ket_1) == ket_0 + ket_1  # True
```

Dirac notation also supports human-readable output with any chosen vectors. The output is a linear combination of vectors `|0>, |1>, ..., |n>` by default, you can also choose decimal precision:

```
>>> dirac.print(ket_0)
|0> = |0>
>>> dirac.print(ket_0, [ket_0, ket_1])
|0> = |0>
>>> dirac.print(ket_0, [fourier_ket_0, fourier_ket_1], precision = 2)
|0> = 0.71 |+> + 0.71 |->
```