from flask import Flask, render_template, request
import sqlite3 as sql
from geopy.geocoders import ArcGIS

app = Flask(__name__)


conn = sql.connect("employees.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, address TEXT NOT NULL)")
conn.commit()


@app.route("/view")
def view():
    conn = sql.connect("employees.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    return render_template("view.html", rows = rows)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/savedetails", methods = ["POST", "GET"])
def savedetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            conn = sql.connect("employees.db")
            cur = conn.cursor()
            # geolocator = ArcGIS()
            # location = geolocator.geocode(address)
            cur.execute("INSERT INTO employees (name, email, address) VALUES(?, ?, ?)",(name, email, address))
            conn.commit()
            msg = "Employee Succesfully Added"
        except:
            conn.rollback()
            msg = "Employee could not be added"
        finally:
            return render_template("success.html", msg = msg)

@app.route("/deleterecord", methods = ["POST"])
def deleterecord():
    msg = "msg"
    if request.method == "POST":
        try:
            id = request.form["id"]
            conn = sql.connect("employees.db")
            cur = conn.cursor()
            # geolocator = ArcGIS()
            # location = geolocator.geocode(address)
            cur.execute("DELETE FROM employees WHERE id=?", (id,))
            conn.commit()
            msg = "Employee Succesfully Deleted"
        except:
            msg = "Employee could not be Deleted"
        finally:
            return render_template("success.html", msg = msg)
            
    



if __name__== "__main__":
    app.run(debug=True)