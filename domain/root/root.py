from flask import render_template



def display():
    return render_template("root/index.html", title="Hellow")