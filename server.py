from flask_app import app
from flask_app.controllers import routes, routes_magazines, routes_users


if __name__ == "__main__":
    app.run(debug=True)

