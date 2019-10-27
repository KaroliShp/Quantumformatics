from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const


class Basis:

    def __init__(self, vectors):
        self.vectors = vectors