# Quantumformatics

Framework for simulating quantum information and computation theory on classic computers.

## Table of Contents

## Example

## Setup

## Dirac notation

Dirac notation is a convenient notation to represent linear algebra concepts, such as row and column vectors, matrices and linear algebra operations. The purpose of Dirac notation in this repository is to increase readability and usability for the users. You can describe and read quantum states in terms of kets and bras, which on computer is way simpler than trying to read multidimensional arrays. Dirac notation implementation uses `numpy` package under the hood to hold the values and perform calculations.

### Design

`Ket` and `Bra` classes represent column and row vectors in d-dimensional Hilbert space, respectively. They are both subtypes of `Matrix` class, which represents a generic matrix. Objects can be created from `list` or `np.ndarray`, `Bra` can also be created from `Ket` (using adjoint operation).

```python
ket_0 = Ket([1, 0]) # |0>
ket_1 = Ket([0, 1]) # |1>

bra_0 = Bra([1, 0]) = Bra(ket_0) # <0|, created from |0>
bra_1 = Bra([0, 1]) = Bra(ket_1) # <1|, created from |1>

identity = Matrix(np.array([[1,0], [0, 1]])) # I
```

You can use arithmetic and comparison operators on these objects and therefore construct new objects:

```python
ket_x = ket_0 + ket_1 # |0> + |1>
type(ket_x) # Ket

ket_y = 2 * ket_01 # 2|0> + 2|1>
type(ket_y) # Ket

product = bra_0 * ket_0 # 1
type(product) # Int
```

You can also construct `Matrix` using `Bra` and `Ket`, or if you wish, you can construct it in a usual way:

```python
matrix = ket_0 * bra_0 # |0><0| = [ 1 0 / 0 0 ]
type(matrix) # Matrix

matrix = Matrix(np.array([[1, 0], [0, 0]])) # [ 1 0 / 0 0 ]
```

You can either use the operators to perform mathematical functions, or you can use functions provided in the `functions.py` file.

```python
ket_x = add(ket_0, ket_1) = ket_0 + ket_1 # |0> + |1>
```
