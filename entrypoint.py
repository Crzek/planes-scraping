from extencions import get_file
from src import create_app


file_conf = get_file()  # carga el archivo de configuracion
app = create_app(file_conf)


if __name__ == '__main__':
    print("************ MODE DEVELOPMENT *************")
    # gunicorn -b 0.0.0.0:5000 entrypoint:app
    app.run(debug=True)
