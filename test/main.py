from flask import Flask


def main(arg):
    pass

app = Flask(__name__)

if __name__ ==  "__main__":
    #solo para develoment
    app.run(port=8000, debug=True)