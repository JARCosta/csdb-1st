#!/usr/bin/python3
from urllib.robotparser import RequestRate
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras

## SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "istnumber"
DB_DATABASE = DB_USER
DB_PASSWORD = "password"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
    DB_HOST,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD,
)

app = Flask(__name__)

@app.route("/")
def root():
    try:
        return render_template("root.html")
    except Exception as e:
        return str(e)  # Renders a page with the error.

@app.route("/a")
def a():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT nome FROM categoria;"
        cursor.execute(query)
        return render_template("a.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route("/new_cat", methods=["POST"])
def new_cat():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cat_name = request.form["cat_name"]
        cat_type = request.form["cat_type"]
        if(cat_type == "Categoria Simples"):
            query = "INSERT INTO categoria VALUES (%s); INSERT INTO categoria_simples VALUES (%s);"
        else:
            query = "INSERT INTO categoria VALUES (%s); INSERT INTO super_categoria VALUES (%s);"
        data = (cat_name, cat_name)
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/add_sub", methods=["POST"])
def add_sub():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sub_name = request.form["sub_name"]
        super_name = request.form["super_name"]
        print(sub_name + " " + super_name)
        query = "INSERT INTO tem_outra VALUES (%s, %s);"
        data = (super_name, sub_name)
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/delete_cat")
def delete_cat():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cat_name = request.args["cat_name"]
        query = """ START TRANSACTION;
                DELETE FROM evento_reposicao WHERE ean = ANY (SELECT ean FROM produto WHERE cat = %s);
                DELETE FROM tem_categoria WHERE nome = %s;
                DELETE FROM planograma WHERE ean = ANY (SELECT ean FROM produto WHERE cat = %s);
                DELETE FROM produto WHERE cat = %s;              
                DELETE FROM responsavel_por WHERE nome_cat = %s;
                DELETE FROM prateleira WHERE nome = %s;
                DELETE FROM tem_outra WHERE super_categoria = %s;
                DELETE FROM tem_outra WHERE categoria = %s;
                DELETE FROM categoria_simples WHERE nome = %s;
                DELETE FROM super_categoria WHERE nome = %s;
                DELETE FROM categoria WHERE nome = %s;
                COMMIT;"""
        data = (cat_name,) * 11
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/b")
def b():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT nome, tin FROM retalhista;"
        cursor.execute(query)
        return render_template("b.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route("/delete_retailer")
def delete_retailer():
    dbConn = None
    cursor = None
    try:
        name = request.args["name"]
        tin = request.args["tin"]
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """START TRANSACTION;
                DELETE FROM evento_reposicao WHERE tin = %s;
                DELETE FROM responsavel_por WHERE tin = %s;
                DELETE FROM retalhista WHERE nome = %s;
                COMMIT;
                """
        data = (tin, tin, name)
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/new_retailer", methods=["POST"])
def new_retailer():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ret_name = request.form["retailer_name"]
        ret_tin = request.form["retailer_tin"]
        query = "INSERT INTO retalhista VALUES (%s, %s);"
        data = (ret_tin, ret_name)
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/c")
def c():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT num_serie, fabricante, nome, concelho, distrito FROM IVM NATURAL JOIN ponto_de_retalho;"
        cursor.execute(query)
        return render_template("c.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route("/events")
def events():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT produto.cat, sum(unidades) FROM evento_reposicao NATURAL JOIN produto WHERE num_serie = %s GROUP BY produto.cat;"
        data = (request.args["ivm"], )
        cursor.execute(query, data)
        return render_template("events.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route("/d")
def d():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM super_categoria;"
        cursor.execute(query)
        return render_template("d.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route("/sub")
def sub():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cat_name = request.args["cat_name"]
        query = """

                WITH filhos AS (
                    SELECT super_categoria, categoria 
                    FROM tem_outra
                    UNION ALL
                    SELECT filho.super_categoria, pai.categoria
                    FROM tem_outra pai
                    INNER JOIN tem_outra filho ON filho.categoria = pai.super_categoria
                )
                SELECT categoria FROM filhos WHERE filhos.super_categoria = %s;
                """
        data = (cat_name, )
        cursor.execute(query, data)
        return render_template("sub.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()


CGIHandler().run(app)
