from flask import Flask,jsonify
import json
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["student_db"]
collection = db["students"]

@app.route("/api",methods=['GET'])
def get_data():
    try:
        with open ("data.json",'r') as file:
            data=json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error":"data.json not found"}),404
    except Exception as e:
        return jsonify({"error":str(e)}),500
@app.route("/")
def home():
    return render_template("todo.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "age": int(request.form["age"])
        }

        collection.insert_one(data)

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("index.html", error=str(e))

    except Exception as e:
        return render_template("index.html", error=str(e))
    
    
@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/submittodoitem",methods=['POST'])
def submittoditem():

    try:
        print("we are inside in try")
        item_name=request.form['itemName']
        item_desc=request.form['itemDesc']
        print("2nd breakpoint")
        todo={
        "itemName":item_name,
        "itemDesc":item_desc
        }
        print("3rd breakpoint")
        collection.insert_one(todo)
        print("4th breakpoint")

        return render_template(
        "todo.html",
        message="To-Do Item Submitted Successfully!"
        )
    
    except Exception as e:
    
        return render_template(
            "todo.html",
            error=str(e)
        )
if __name__=="__main__":
    app.run(debug=True)

