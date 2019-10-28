from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const

class Composition:

    def __init__(self, state: Ket, systems: list):
        self.state = state
        self.systems = systems

        self.is_entangled()

    
    def is_entangled(self):
        pass