class User:
    def __init__(self, user_id: int, okato: str):
        self.user_id = user_id
        self.okato = okato

    def tuple(self):
        return self.user_id, self.okato
