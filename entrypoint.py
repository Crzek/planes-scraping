import os
from src import create_app


def get_file() -> str:
    name = os.getenv("CONFIG_ENV")
    print("***getenv**8", name)
    if (name == "development"):
        return "config/dev.py"
    else:  # (name == "production")
        return "config/prod.py"


file_conf = get_file()
print("***file_conf***", file_conf)
app = create_app(file_conf)

if __name__ == '__main__':
    print("************ MODE DEVELOPMENT *************")
    # gunicorn -b 0.0.0.0:5000 entrypoint:app
    app.run(debug=True)
