import firebase_admin
from flask import Flask, render_template, request, redirect
from firebase_admin import credentials, firestore

cred = credentials.Certificate("config/firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["long_url"]
        doc_ref = db.collection("urls").add({"long_url": long_url})
        short_id = doc_ref[1].id
        short_url = f"{request.host_url}{short_id}"
        return render_template("index.html", short_url=short_url)
    else:
        return render_template("index.html")

@app.route("/<short_id>", methods=["GET"])
def redirect_to_long_url(short_id):
    try:
        doc_ref = db.collection("urls").document(short_id)
        doc = doc_ref.get()
        if doc.exists:
            long_url = doc.to_dict()["long_url"]
            return redirect(long_url)
        else:
            return "Error: URL cannot be found", 404
    except Exception as e:
        return str(e), 500