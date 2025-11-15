class Measure:
    def __init__(
            self,
            measure_id: str,
            okato: str,
            name: str,
            duration: str,
            documents: str,
            procedure: str,
            result: str,
            link: str | None
    ):
        self.measure_id = measure_id
        self.okato = okato
        self.name = name
        self.duration = duration
        self.documents = documents
        self.procedure = procedure
        self.result = result
        self.link = link

    def tuple(self):
        return (
            self.measure_id,
            self.okato,
            self.name,
            self.duration,
            self.documents,
            self.procedure,
            self.result,
            self.link
        )
