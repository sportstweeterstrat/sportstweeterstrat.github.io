from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import db

app = Flask(__name__)

def initialize_db():
    cert = firebase_admin.credentials.Certificate("sports-tweeter-strat-c141d-firebase-adminsdk-ci2eq-3c60f98ce1.json")
    default_app = firebase_admin.initialize_app(cert, {'databaseURL':"https://sports-tweeter-strat-c141d-default-rtdb.firebaseio.com/"})


def generate_keys_firebase():
    users_ref = db.collection(u"waitlist")
    docs = users_ref.stream()
    cache = {}
    for doc in docs:
        cache[doc.id] = 1
    return cache


@app.route("/", methods=["GET"])
def home():
    initialize_db()
    return render_template("signup.html")


@app.route("/email", methods=["POST"])
def email():
    ref = db.reference("/")
    email = request.form.get("home")
    dict = ref.get()
    for val in dict.values():
        if email == val:
            return render_template("signup.html")
    ref.push().set(email)
    return render_template("signup.html")


if __name__ == "__main__":
    app.run()
