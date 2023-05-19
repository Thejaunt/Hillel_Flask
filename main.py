from flask import Flask, url_for
import csv
from statistics import mean
from faker import Faker
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return f"""
            <p><a href='{url_for('get_requirements')}'>REQUIREMENTS. Installed Modules</a></p>
            <p><a href='{url_for('generate_users')}'>Users Generator</a></p>
            <p><a href='{url_for('average_height_weight')}'>Average Height&Weight</a></p>
            <p><a href='{url_for('get_curr_spacemen')}'>Spacemen in the outerspace</a></p>
"""


@app.route("/requirements/")
def get_requirements():
    req = list()
    with open("requirements.txt", "r") as rf:
        for line in rf:
            req.append(line)

    return f"<h1>Installed Modules</h1>{'<br>'.join([x for x in req])}"


@app.route("/generate-users/")
@app.route("/generate-users/<int:count>")
def generate_users(count: int = 100):
    fake = Faker()
    data_dict = dict()
    for _ in range(count):
        data_dict[f"{fake.ascii_email()}"] = fake.name()

    output_users_data = str()
    for name, email in data_dict.items():
        output_users_data += f"<p><b>Name:</b> {name} <b>Email:</b> {email}</p>"

    return f"<h1>Random Users</h1>{output_users_data}"


@app.route("/mean/")
def average_height_weight():
    hw_data = "hw.csv"
    height_data: list[float] = []
    weight_data: list[float] = []
    with open(hw_data) as f:
        data = csv.DictReader(f)
        for row in data:
            height_data.append(float(row[' "Height(Inches)"']))
            weight_data.append(float(row[' "Weight(Pounds)"']))

    average_height_inc = mean(height_data)
    average_weight_lbs = mean(weight_data)
    average_height_cm = round(average_height_inc * 2.54, 2)
    average_weight_kg = round(average_weight_lbs * 0.453592, 2)

    return f"Average height is - {average_height_cm}cm<br>Average weight is - {average_weight_kg}kg"


@app.route("/space/")
def get_curr_spacemen():
    resp = requests.get("http://api.open-notify.org/astros.json")
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as er:
        return f"[ERROR] the homework went wrong {er}"
    data = resp.json()
    try:
        spacemen_amount = len(data["people"])
    except KeyError:
        return "[ERROR] couldn't get the data"

    return f"There are {spacemen_amount} spacemen in the outerspace"
