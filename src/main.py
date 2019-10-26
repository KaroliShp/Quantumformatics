from src.dirac.bra import Bra
from src.dirac.ket import Ket
from src.dirac.matrix import Matrix
from src import constants


if __name__ == '__main__':
    # Standard
    print('\n')
    comp_ket_0 = constants.comp_ket_x(0, 2)
    print(comp_ket_0)
    comp_ket_1 = constants.comp_ket_x(1, 2)
    print(comp_ket_1)

    fourier_ket_0 = constants.fourier_ket_x(0, 2)
    print(fourier_ket_0)
    fourier_ket_1 = constants.fourier_ket_x(1, 2)
    print(fourier_ket_1)

    fourier_bra_0 = constants.fourier_bra_x(0, 2)
    print(fourier_bra_0)
    fourier_bra_1 = constants.fourier_bra_x(1, 2)
    print(fourier_bra_1)

    """
    # Kets
    print('\n')
    ket_0 = Ket([1, 0])
    print(ket_0)
    print(ket_0 == st_ket_0)

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
    """