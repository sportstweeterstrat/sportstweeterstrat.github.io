from flask import Flask, render_template, request
import firebase_admin
import boto3
import json
from firebase_admin import db

app = Flask(__name__)

PERMISSIONS_BUCKET = 'sports-tweeter-permissions'
s3 = boto3.client('s3')

def initialize_db():
    s3_cert_obj = s3.get_object(Bucket=PERMISSIONS_BUCKET, Key="sports-tweeter-strat-c141d-firebase-adminsdk-ci2eq-3c60f98ce1.json")
    s3_cert_str = s3_cert_obj['Body'].read().decode('utf-8')
    s3_cert_str.replace("\n", "")
    s3_cert = json.loads(s3_cert_str)
    cert = firebase_admin.credentials.Certificate(s3_cert)
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
    return render_template("index.html")


@app.route("/email", methods=["POST"])
def email():
    ref = db.reference("/")
    email = request.form.get("home")
    dict = ref.get()
    for val in dict.values():
        if email == val:
            return render_template("index.html")
    ref.push().set(email)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
