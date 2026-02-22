from src import create_app
 
 
 
app = create_app()


if __name__ == '__main__':
    print("************ MODE DEVELOPMENT *************")
    # gunicorn -b 0.0.0.0:5000 entrypoint:app
    app.run(debug=True, loat_env=".env.chrome")
