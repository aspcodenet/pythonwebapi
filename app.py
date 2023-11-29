from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, seedData, Customer
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate, upgrade
import os

app = Flask(__name__)
if os.getenv('RUNENVIRONMENT') == "Production":
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

# Go -> ORM -> GORM 
# code first
db.app = app 
db.init_app(app)
migrate = Migrate(app,db)


@app.route("/")
def homePage():
    s = "<html><head><title>Hej</title></head><body><h1>Hallo</h1><p>Tjena</p></body></html>"
    return s


@app.route("/api/customer/<id>", methods=["PUT"])
def apiCustomerUpdate(id):
    data = request.get_json()
    c = Customer.query.filter_by(Id=id).first_or_404()
    c.City = data["City"]
    c.Name = data["Name"]
    c.Telephone = data["Telephone"]
    c.TelephoneCountryCode = data["TelephoneCountryCode"]
    db.session.commit()
    return jsonify({ "Id": c.Id, 
                 "Name":c.Name, 
                 "City":c.City,
                  "TelephoneCountryCode":c.TelephoneCountryCode,
                   "Telephone":c.Telephone }), 200

@app.route("/api/customer", methods=["POST"])
def apiCustomerCreate():
    data = request.get_json()
    c = Customer()
    c.City = data["City"]
    c.Name = data["Name"]
    c.Telephone = data["Telephone"]
    c.TelephoneCountryCode = data["TelephoneCountryCode"]
    db.session.add(c)
    db.session.commit()
    return jsonify({ "Id": c.Id, 
                 "Name":c.Name, 
                 "City":c.City,
                  "TelephoneCountryCode":c.TelephoneCountryCode,
                   "Telephone":c.Telephone }), 201

# fler funktioner
# RESTAPI - C R U D
# Dockerfile

@app.route("/api/customer/<id>")
def apiCustomer(id):
    c = Customer.query.filter_by(Id=id).first_or_404()
    # select * from customer where id=@id
    return jsonify({ "Id": c.Id, 
                 "Name":c.Name, 
                 "City":c.City,
                  "TelephoneCountryCode":c.TelephoneCountryCode,
                   "Telephone":c.Telephone })


@app.route("/api/customer")
def apiCustomers():
    lista = []
    for c in Customer.query.all():
        cdict = { "Id": c.Id, 
                 "Name":c.Name, 
                 "City":c.City }
        lista.append(cdict)
 
    return jsonify(lista)    

with app.app_context():
    db.create_all()
    seedData(db)
    app.run()