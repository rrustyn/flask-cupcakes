"""Flask app for Cupcakes"""
from flask import Flask, request, url_for, render_template, redirect, flash, jsonify

from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SECRET_KEY'] = "hunter2"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
db.create_all()

############################################################
# Routes


@app.get("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id,flavor,size,rating,image},...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def show_capcake_info(cupcake_id):
    """Return JSON {'cupcake': {id,flavor,size,rating,image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Return JSON {'cupcake': {id,flavor,size,rating,image}}"""

    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"]
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized= cupcake.serialize()

    return (jsonify(cupcake= serialized), 201)