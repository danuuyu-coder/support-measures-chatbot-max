class Region:
    def __init__(self, okato: str, name: str):
        self.okato = okato
        self.name = name

    def tuple(self):
        return self.okato, self.name
