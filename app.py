from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route("/")
def hello_world():
    return "Bisal_Files with SQLite"

@app.route("/files", methods=["GET", "POST"])
def manage_files():
    if request.method == "POST":
        data = request.get_json()
        new_file = File(name=data["name"], size=data["size"])
        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message": "File added!"}), 201
    else:
        files = File.query.all()
        result = [{"id": file.id, "name": file.name, "size": file.size} for file in files]
        return jsonify(result)

if __name__ == "__main__":
    app.run()
