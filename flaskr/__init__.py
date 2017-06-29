#!/usr/bin/python3
# -*- coding: latin-1 -*-

#NOMBRE COLECCION = coleccion
#NOMBRE DB = dbName

import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "myDatabase"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

'''# Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = ""
POSTGRESUSER = ""
POSTGRESPASS = ""
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''


#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


@app.route("/mongob")  # adicional para devolver json sin templates
def mongob():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results


@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/fecha")
def fecha():
    fecha = request.args.get("fecha")
    results = eval('mongodb.'+ 'coleccion.find({"fecha":"'+fecha+'"}, {"numero": 1, "_id":0})')
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results

@app.route("/kmensajes")
def kmensajes():
    k = request.args.get("k")
    numero = request.args.get("numero")
    results = eval('mongodb.coleccion.find({"numero":"'+numero+'"},{"contenido":1, "_id":0}).sort("fecha",-1).limit('+k+')')
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results
@app.route("/pclave")
def pclave():
    clave = request.args.get("clave")
    results = eval('mongodb.coleccion.find({"$text": {"$search": "'+clave+'"}},{"_id":0})')
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return results




@app.route("/example")
def example():
    return "lol"  # render_template('example.html')


# funciones particulares

# Dada una fecha, todos los numeros para los que se tienen mensajes en esa fecha
# pagina de la forma: query17-23.ing.puc.cl/fecha?fecha=2016-10-24



if __name__ == "__main__":
    app.run()
