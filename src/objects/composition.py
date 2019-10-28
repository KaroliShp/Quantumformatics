class Composition:

    def __init__(self, state: Ket, systems: list):
        self.state = state
        self.systems = systems

        self.is_entangled()

    
    def is_entangled(self):
        pass