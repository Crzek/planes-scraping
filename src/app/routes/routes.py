from flask import render_template, request, redirect, url_for

from src.app import scrapping_bp


@scrapping_bp.route('/')
def index():

    # boton para ejecutar la funcion de aviones
    return render_template('index.html')


@scrapping_bp.route('/aviones/<string:day>', methods=['POST'])
def exec(day: str = 'today'):
    """
    ejecuta la funcion exec_aviones

    input :
    return :
    """
    if day == 'today':
        exect_aviones(True)

    # ejecutar para mañana
    else:
        exect_aviones(False)


    return redirect(url_for('scrapBP.index'))


# funcion par aejecutar aviones
def exect_aviones(today: bool = True):
    """
    progrma que ejecuta la funcion de aviones,
    optiene los datos de la pagina web de aviones

    input :
    return :
    """
    # dar stylos al excel
    from src.app.utils.styles import main_styles
    from src.app.main import main

    hoy = today
    main(hoy)
    main_styles(hoy)
