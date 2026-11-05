class ApiError(Exception):
    """Fallo de la ruta API que debe activar el fallback a Playwright.

    El mensaje describe el motivo sin incluir credenciales, tokens ni
    cuerpos de peticion/respuesta.
    """

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason
