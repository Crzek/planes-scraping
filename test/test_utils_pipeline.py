import pytest

from src.app.models.aircraft import AirCraft
from src.app.utils import utils
from src.app.utils.utils import get_all_reservas, save_Book_by_tag


@pytest.fixture(autouse=True)
def limpio():
    AirCraft.all_reservas = {}
    utils.BOOKS.clear()
    yield
    AirCraft.all_reservas = {}
    utils.BOOKS.clear()


TITLES = [
    "09:00 - 10:30\nEC-FED\nPERSONA UNO\nDUAL / PIC",
    "11:00 - 12:30\nEC-FED\nPERSONA DOS\nPIC",
    "10:00 - 11:00\nEC-ERV\nPERSONA TRES\nDUAL",
]


def test_save_book_by_tag_acumula_salidas_y_llegadas():
    assert all(save_Book_by_tag(t) for t in TITLES)
    assert AirCraft.all_reservas == {
        # la llegada conserva el prefijo "- " (hora[6:]); no se usa en las tablas
        "EC-FED": {"takeoff": ["09:00", "11:00"],
                   "landing": ["- 10:30", "- 12:30"]},
        "EC-ERV": {"takeoff": ["10:00"], "landing": ["- 11:00"]},
    }


def test_save_book_by_tag_cadena_incompleta_devuelve_false_o_falla():
    with pytest.raises(ValueError):
        save_Book_by_tag("09:00 - 10:30")


def test_aviones_excluidos_no_aparecen_en_las_tablas():
    save_Book_by_tag("09:00 - 10:30\nES-3A-042\nX\nPIC")
    save_Book_by_tag("09:00 - 10:30\nEC-FED\nY\nPIC")
    data = get_all_reservas(AirCraft.all_reservas)
    assert "ES-3A-042" not in data["books"]
    assert "EC-FED" in data["books"]
