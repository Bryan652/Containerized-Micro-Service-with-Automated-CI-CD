from flask import Flask, request, render_template, redirect, url_for
from db import ConnToData
from db_seeder import seed_database

BookAPI = Flask(__name__)

# HOME 
@BookAPI.route("/", methods=["GET"])
def Home(): 
    get_data = ConnToData(0)
    return render_template("index.html", datas=get_data)

# CRUD
@BookAPI.route("/Add", methods=['POST'])
def Add():
    name=request.form.get("Name")
    year=request.form.get("Year")
    author=request.form.get("Author")

    ConnToData(cond=3,Name=name,Year=year,Author=author)

    return redirect(url_for('Home'))

@BookAPI.route("/Update/<int:id>", methods=['POST'])
def Update(id):     
    name=request.form.get("Name")
    year=request.form.get("Year")
    author=request.form.get("Author")

    ConnToData(cond=1, id=id, Name=name,Year=year,Author=author)

    return redirect(url_for('Home'))

@BookAPI.route("/Delete/<int:id>", methods=['POST'])
def Delete(id):
    ConnToData(cond=2, id=id)
    
    return redirect(url_for('Home'))

@BookAPI.route("/Seed", methods=['POST'])
def Seed():
    seed_database()

    return redirect(url_for('Home'))

# ERRORS
@BookAPI.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@BookAPI.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# START
def StartAPI():
    BookAPI.run(debug=False, host="0.0.0.0", port=5000)