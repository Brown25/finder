import os
from flask import Flask, render_template
from tracking import Package

app = Flask(__name__)

@app.route("/")
def index():
    # Example usage of the Package class
    package = Package(
        tracking_number="1234567890",
        tracking_url="http://tracking.example.com/1234567890",
        support_phone_numbers=["123-456-7890", "098-765-4321"]
    )
    package.set_create_date("2023-05-01 10:00:00")
    package.set_promised_date("2023-05-05")
    package.add_transit_event("2023-05-02 12:00:00", "City A, State A, Country A")
    package.add_transit_event("2023-05-03 15:00:00", "City B, State B, Country B")

    package_info = package.get_info()

    # Render the package information (you can pass it to your template)
    return render_template('index.html', package_info=package_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
