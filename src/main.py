# src/main.py

import os
from flask import Flask, render_template, request
from datetime import datetime
from database import Database
from models import Package, TransitEvent
from tracking import PackageInfo

app = Flask(__name__)

# Set up the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = Database(app)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    package_info = None
    if request.method == "POST":
        tracking_number = request.form.get("tracking_number")
        password = request.form.get("password")

        package = Package.query.filter_by(tracking_number=tracking_number).first()
        if package and password == "example_password":  # Simplified password check
            package_info = PackageInfo(
                tracking_number=package.tracking_number,
                tracking_url=package.tracking_url,
                support_phone_numbers=package.support_phone_numbers.split(","),
                create_date=package.create_date,
                promised_date=package.promised_date,
                transit_events=[{"timestamp": event.timestamp, "location": event.location} for event in package.transit_events]
            )
        else:
            error = "Invalid tracking number or password."

    current_time = datetime.now().strftime("%A %b %d, %Y, %H:%M:%S")
    return render_template("index.html", error=error, package_info=package_info, current_time=current_time)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
