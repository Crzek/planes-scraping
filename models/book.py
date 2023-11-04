from .aircraft import AirCraft


class Books:
    reservas: list = []


class Book:

    def __init__(self, salida, llegada, persona, plane) -> None:
        self.landing = salida
        self.takeoff = llegada
        self.persona = persona
        self.plane: AirCraft = plane
