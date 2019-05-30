from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import time
import random
import json

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "finalpython"
client = MongoClient(
    "mongodb://deyxon:mafalu04@ds157956.mlab.com:57956/finalpython")
db = client.finalpython
app.secret_key = 'myscretkey'


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/add-guarda')
def view_Add():
    return render_template('add-guarda.html')


@app.route('/guarda', methods=['POST'])
def add_guarda():
    if request.method == 'POST':
        idg = request.form['idg']
        nombre = request.form['nombreg']
        newGuarda = {
            "nombre": nombre,
            "id": idg,
            "infracciones": []
        }
        guarda = db.guardas.insert_one(newGuarda)
        flash('Guarda guardado correctamente')
        return redirect(url_for('List'))


@app.route('/lst-guards')
def List():
    data = []
    cursor = db.guardas.find()
    for doc in cursor:
        data.append(doc)
    return render_template('lst-guardas.html', guarda=data)


@app.route('/detail-guarda/<id>')
def AddInfra(id):
    data = []
    guarda = db.guardas.find_one({"id": id})
    return render_template('add-infra.html', guarda=guarda)


@app.route('/view-guarda/<id>')
def ViewInfo(id):
    guarda = db.guardas.find_one({"id": id})
    return render_template('view.info.html', guarda=guarda)


@app.route('/detail-summary', methods=['POST'])
def detal_summary():
    if request.method == 'POST':
        type_infraccion = request.form['tipe']
        print(type_infraccion)
        infracciones = []
        cursor = db.infracciones.find()
        for doc in cursor:
            if doc['concepto'] == type_infraccion:
                if len(infracciones) == 0:
                    infracciones.append(doc)
                else:
                    for doc1 in infracciones:
                        if doc1.get(doc['idguarda']) == None:
                            infracciones.append(doc)

        for doc in infracciones:
            cursor = db.infracciones.find(
                {"idguarda": doc['idguarda'], "concepto": type_infraccion}).count()
            print(cursor)
            pass
    return render_template('detal-summary.html', data=type_infraccion, inf=infracciones)


@app.route('/summary')
def Summary():

    return render_template('summary.html')


@app.route('/add-info/<id>/<nombre>', methods=['POST'])
def addinfra(id, nombre):
    if request.method == 'POST':
        documentToSupdate = {
            "id": random.randrange(1000),
            "placa": request.form['placa'],
            "identificacion": request.form['identificacion'],
            "fecha": time.strftime("%d/%m/%y"),
            "nombre": request.form['nombre'],
            "valor": request.form['valor'],
            "concepto": request.form['concepto']
        }
        guardas = db.guardas.update_one(
            {"id": id}, {"$push": {"infracciones": documentToSupdate}})
        documentToSupdate['idguarda'] = id
        documentToSupdate['nombreg'] = nombre
        db.infracciones.insert_one(documentToSupdate)
        return redirect(url_for('List'))


if __name__ == '__main__':
    app.run(port=4800, debug=True)
