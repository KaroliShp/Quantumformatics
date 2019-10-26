from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation.vector import Vector

if __name__ == '__main__':
    # Kets
    print('\n')
    ket_0 = Ket([1, 0])
    print(ket_0)

    ket_1 = Ket([0, 1])
    print(ket_1)

    ket_x = Ket([-2, 1])
    print(ket_x)

    ket_complex = Ket([1 + 1j, -1 - 1j])
    print(ket_complex)

    # Bra
    print('\n')
    bra_0 = Bra([1, 0])
    print(bra_0)

    bra_0 = Bra(ket_0)
    print(bra_0)

    bra_complex = Bra(ket_complex)
    print(bra_complex)

    # Arithmetics
    print('\n')
    print(ket_0 + ket_1)
    print(ket_0 * 2)
    print(-2 * ket_0)
    print(ket_0 / 2)

    print(bra_0 + Bra(ket_1))
    print(bra_0 * ket_0)
    #print(ket_0 * ket_0)
    print(ket_0 * bra_0)

    # Comparison
    print('\n')
    print(ket_0 == ket_1)
    print(ket_0 != ket_1)
    print(ket_0 == ket_0)