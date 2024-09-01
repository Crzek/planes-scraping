class AirCraft:
    all_reservas: dict = {}

    def __init__(self, codigo, estado=None) -> None:
        self.modelo: str = codigo  # codigo avion
        self.reservas: dict = {}
        if estado != None:             # si esta en mantenimiento
            self.estado = estado
        else:
            self.estado = estado

    @classmethod
    def add_reservas(cls, reserva):
        cls.all_reservas.append(reserva)

    @classmethod
    def get_reservas(cls):
        return AirCraft.all_reservas

    def update_reservas(self, takeoff_n: str, landing_n: str):
        if self.modelo in AirCraft.all_reservas:  # SI SE ECUENTRA , SOLO aCTUALIZAR
            takeoffANDlanding: dict = AirCraft.all_reservas[self.modelo]
            takeoffANDlanding["takeoff"].append(takeoff_n)
            takeoffANDlanding["landing"].append(landing_n)

        else:  # CREAR OBJ
            AirCraft.all_reservas[self.modelo] = {
                "takeoff": [takeoff_n],
                "landing": [landing_n],
            }
        self.reservas: dict = {
            "takeoff": takeoff_n,
            "landing": landing_n,
        }
