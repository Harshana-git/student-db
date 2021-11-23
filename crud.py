from flask import Flask, render_template
from flask import *
import sqlite3
import os

template_dir = os.path.abspath('./')
app = Flask(__name__, template_folder=template_dir)
@app.route("/")
def index():
 return render_template("index.html")

@app.route("/add")
def add():
 return render_template("add.html")

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
 msg = "msg"
 if request.method == "POST":
  try:
   name = request.form["name"]
   email = request.form["email"]
   address = request.form["address"]
   with sqlite3.connect("Student.db") as con:
    cur = con.cursor()
    cur.execute("INSERT into Student (name, email, address) values (?,?,?)",(name,email,address))
    con.commit()
    msg = "Student successfully Added"
  except:
    con.rollback()
    msg = "We can not add the Student to the list"
  finally:
   return render_template("success.html", msg=msg)


@app.route("/view")
def view():
 con = sqlite3.connect("Student.db")
 con.row_factory = sqlite3.Row
 cur = con.cursor()
 cur.execute("select * from Student")
 rows = cur.fetchall()
 return render_template("view.html", rows=rows)


@app.route("/delete")
def delete():
 return render_template("delete.html")

@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
 id = request.form["id"]
 with sqlite3.connect("Student.db") as con:
  try:
   cur = con.cursor()
   cur.execute("delete from Student where id = ?",id)
   msg = "record successfully deleted"
  except:
   msg = "can't be deleted"
  finally:
   return render_template("delete_record.html", msg=msg)

if __name__ == "__main__":
 app.run(debug=True)




