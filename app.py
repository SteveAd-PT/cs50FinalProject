import os
from flask import Flask, flash, redirect, render_template, request
import sqlite3

# Configure application
app = Flask(__name__)
app.secret_key = 'dev'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Home
@app.route('/')
def index():
    return render_template("index.html")

# Alle Einträge
@app.route("/all", methods=["POST", "GET"])
def all():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row 
    cur = con.cursor()
    cur.execute("SELECT * FROM project")
    rows = cur.fetchall()
    suche = "Alle Vögel des Jahres:"
    return render_template("search.html", datas = rows, suche = suche)

# Suche per Formular (mit ein oder beiden Selector)
@app.route("/search", methods=["POST", "GET"])
def search():
    # Def der Suchwerte
    größe = int(request.form.get("big"))
    größeMinus = größe - 9
    größePlus = größe + 1
    weite = int(request.form.get("span"))
    weiteMinus = weite - 9
    weitePlus = weite + 1
    # Verbindung mit Datenbank
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row 
    cur = con.cursor()
    # Suche ohne Sucheinträge
    if weite == 100 and größe == 100:
        flash('Keine Suchwerte')
        return redirect("/")
    # Suche mit beiden Selector
    elif weite != 100 and größe != 100:
        suche = "Nach Größe und Spannweite gefiltert:"    
        cur.execute("SELECT * FROM project WHERE spannsuche IN (?, ?, ?) AND größesuche IN (?, ?, ?)", (weite, weiteMinus, weitePlus, größe, größeMinus, größePlus))
        if (cur.fetchone()) is None:
            flash('Keine Suchergebnisse')
            return redirect("/")
        else:
            cur.execute("SELECT * FROM project WHERE spannsuche IN (?, ?, ?) AND größesuche IN (?, ?, ?)", (weite, weiteMinus, weitePlus, größe, größeMinus, größePlus))
            rows = cur.fetchall()
            return render_template("search.html", datas = rows, suche = suche)
    # Suche über Spannweite
    elif größe == 100 and weite != 100:
        suche = "Nach Spannweite gefiltert:"
        cur.execute("SELECT * FROM project WHERE spannsuche IN (?, ?, ?)", (weite, weiteMinus, weitePlus))
        if (cur.fetchone()) is None:
            flash('Keine Suchergebnisse')
            return redirect("/")
        else:
            cur.execute("SELECT * FROM project WHERE spannsuche IN (?, ?, ?)", (weite, weiteMinus, weitePlus))
            rows = cur.fetchall()
            return render_template("search.html", datas = rows, suche = suche)
    # Suche über Größe
    elif weite == 100 and größe != 100:
        suche = "Nach Größe gefiltert:"
        cur.execute("SELECT * FROM project WHERE größesuche IN (?, ?, ?)", (größe, größeMinus, größePlus))
        if (cur.fetchone()) is None:
            flash('Keine Suchergebnisse')
            return redirect("/")
        else:
            cur.execute("SELECT * FROM project WHERE größesuche IN (?, ?, ?)", (größe, größeMinus, größePlus))
            rows = cur.fetchall()
            return render_template("search.html", datas = rows, suche = suche)
# Suche über Searchbox
@app.route("/searchName", methods=["POST", "GET"])
def searchName():
    frage = request.form.get("name")
    frage = frage.lower()
    if not frage:
        flash('Keine Sucheingabe')
        return redirect("/")
    else:
        suche = "Direktsuche:"
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM project WHERE name LIKE ?", (frage,))
        if (cur.fetchone()) is None:
            flash('Keine Suchergebnisse')
            return redirect("/")
        else:
            cur.execute("SELECT * FROM project WHERE name LIKE ?", (frage,))
            rows = cur.fetchall()
            return render_template("search.html", datas = rows, suche = suche)


if __name__ == '__main__':
    app.run()

