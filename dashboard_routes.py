from flask import Blueprint

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def hello():
    return "Hello World"