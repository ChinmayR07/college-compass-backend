from flask import Flask
from flask_cors import CORS
from dashboard_routes import dashboard

app = Flask(__name__)
CORS(app)
app.register_blueprint(dashboard)