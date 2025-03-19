from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# โหลดข้อมูลจาก Excel
EXCEL_FILE = "uploads/data.xlsx"

def load_users():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Users")
    return df.set_index("UserID").to_dict(orient="index")

users = load_users()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userid = request.form["userid"]
        password = request.form["password"]
        
        if userid in users and users[userid]["Password"] == password:
            session["user"] = users[userid]
            return redirect(url_for("dashboard"))
        else:
            return "Login Failed"
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
