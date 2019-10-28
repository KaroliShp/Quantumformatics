from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const


class Basis:

    def __init__(self, vectors: list):
        # Check that the vectors form an ONB
        vectors = np.array(vectors)
        assert vectors.transpose() * vectors == const.identity_matrix

        self.vectors = vectors
        self.vector_space = vectors.shape[0]