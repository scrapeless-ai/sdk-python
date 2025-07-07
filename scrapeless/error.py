class ScrapelessError(Exception):
    def __init__(self, message: str):
        super().__init__(f"[Scrapeless]: {message}")
        self.name = 'ScrapelessError'
        Exception(f"[Scrapeless]: {message}")
