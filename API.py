from flask import Flask, jsonify, redirect, render_template, request, url_for

from db import ConnToData
from db_seeder import seed_database

BookAPI = Flask(__name__)

# PUTE API
@BookAPI.route("/api/books", methods=["GET"])
def api_books():
    return jsonify(ConnToData(0))

@BookAPI.route("/api/books/<int:id>", methods=["GET"])
def api_get_specific_book(id):
    book = next((b for b in ConnToData(0) if b["id"] == id), None)

    if book: 
        return jsonify(book)
    else: 
        return jsonify({"Message":"No specific book with that id found"}), 404

@BookAPI.route("/api/books", methods=["POST"])
def api_add_book():
    data = request.get_json()

    if not data:
        return jsonify({"error" : "Invalid or missing json payload"}), 400

    name = data.get("Name")
    year = data.get("Year")
    author = data.get("Author")

    if not name or not year or not author:
        return jsonify({"error":"Missing required fields"})

    ConnToData(cond=3, Name=name, Year=year, Author=author)

    return jsonify({
        "Message": "Book added successfully",
        "data" : {
            "Name":name,
            "Year":year,
            "Author":author
        }
    }), 201

@BookAPI.route("/api/books/<int:id>", methods=["PUT"])
def api_update_specific_book(id):
    data = request.get_json()

    if not data:
        return jsonify({"error" : "Invalid or missing json payload"}), 400

    name = data.get("Name")
    year = data.get("Year")
    author = data.get("Author")

    ConnToData(cond=1, id=id, Name=name, Year=year, Author=author)

    return jsonify({
        "Message": "Book updated successfully",
        "data": {
            "id":id,
            "Name":name,
            "Year":year,
            "Author":author
        }
    }), 200
    
@BookAPI.route("/api/books/<int:id>", methods=["DELETE"])
def api_delete_specific_book(id):
    ConnToData(cond=2, id=id)

    return jsonify({"Message":f"Book {id} successfully deleted"}), 200

# WITH UI 
@BookAPI.route("/", methods=["GET"])
def home(): 
    get_data = ConnToData(0)
    return render_template("index.html", datas=get_data)

@BookAPI.route("/add", methods=['POST'])
def add():
    name=request.form.get("Name")
    year=request.form.get("Year")
    author=request.form.get("Author")

    ConnToData(cond=3,Name=name,Year=year,Author=author)

    return redirect(url_for('home'))

@BookAPI.route("/update/<int:id>", methods=['POST'])
def update(id):     
    name=request.form.get("Name")
    year=request.form.get("Year")
    author=request.form.get("Author")

    ConnToData(cond=1, id=id, Name=name,Year=year,Author=author)

    return redirect(url_for('home'))

@BookAPI.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    ConnToData(cond=2, id=id)
    
    return redirect(url_for('home'))

@BookAPI.route("/seed", methods=['POST'])
def seed():
    seed_database()

    return redirect(url_for('home'))

# ERRORS
@BookAPI.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@BookAPI.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# START
def StartAPI():
    BookAPI.run(debug=False, host="0.0.0.0", port=5000)