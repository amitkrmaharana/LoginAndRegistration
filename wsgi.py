from application import create_app, database

app = create_app()


if __name__ == '__main__':
    database.create_all()
    app.run(debug=True)
